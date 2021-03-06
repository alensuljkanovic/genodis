import os
from textx.metamodel import metamodel_from_file
from .obj_processors import model_processor, class_processor, \
    property_processor, action_processor, property_argument_processor

__author__ = 'Alen Suljkanovic'


class Model(object):

    """
    Python representation of model defined in grammar.
    """

    def __init__(self, name, classes, actions=None, bindings=None):
        """
        Initialization of model
        """
        super(Model, self).__init__()

        self.name = name
        self.classes = classes
        self.actions = actions if actions else []
        self.bindings = bindings if bindings else []

    def __str__(self):
        return "Model(%s), entities: %s, actions %s" % (self.name,
                                                        self.classes,
                                                        self.actions)


class Class(object):

    """
    Python representation of entity defined in grammar.
    """

    def __init__(self, parent, name, properties, session, actions=None,
                 bindings=None):
        """
        Initialization of entity.
        """
        super(Class, self).__init__()

        self.parent = parent
        self.name = name
        self.properties = properties
        self.actions = actions if actions else []
        self.session = True if session else False
        self.bindings = bindings if bindings else []

        # Dictionary that describes relationship of one class with others.
        # Key is name of referenced class and value shows how many times
        # given class has been referenced.
        self.references = {}

        self.foreign_key = None

    def __str__(self):
        return self.name


class Property(object):

    """
    Python representation of property defined in grammar.
    """

    def __init__(self, parent, name, type, list=None, arguments=None):
        """
        Initialization of property.
        """
        super(Property, self).__init__()

        self.parent = parent
        self.name = name
        self.type = type
        self.list = True if list else False
        self.arguments = arguments if arguments else []

    def __str__(self):
        return self.name

    @property
    def args_dict(self):
        args = {arg.name: arg for arg in self.arguments}
        return args


class PropertyArgument(object):

    """
    Python representation of property argument defined in grammar.
    """

    def __init__(self, parent, unique=None, unique_value=None,
                 readonly=None, readonly_value=None,
                 required=None, required_value=None,
                 min_length=None, min_length_value=None,
                 max_length=None, max_length_value=None,
                 choices=None, choices_value=None,
                 calc=None, calc_value=None,
                 decimal_places=None, decimal_places_value=None,
                 max_digits=None, max_digits_value=None):
        """
        Initialization of property argument.
        """
        super(PropertyArgument, self).__init__()

        self.parent = parent
        self.unique = unique
        self.unique_value = unique_value
        self.readonly = readonly
        self.readonly_value = readonly_value
        self.required = required
        self.required_value = required_value
        self.min_length = min_length
        self.min_length_value = min_length_value
        self.max_length = max_length
        self.max_length_value = max_length_value
        self.choices = choices
        self.choices_value = choices_value
        self.calc = calc
        self.calc_value = calc_value
        self.max_digits = max_digits
        self.max_digits_value = max_digits_value
        self.decimal_places = decimal_places
        self.decimal_places_value = decimal_places_value

        self._value = None

    def __str__(self):
        if self.required:
            return "blank=%s" % self.value
        elif not self.choices:
            return "%s=%s" % (self.name, self.value)
        else:
            ret = tuple((data.key, data.name) for data in self.choices_value)
            return "%s=%s" % (self.name, ret)

    @property
    def name(self):
        """
        Returns the name of the property argument.
        """
        if self.unique:
            return "unique"
        elif self.readonly:
            return "readonly"
        elif self.required:
            return "required"
        elif self.min_length:
            return "min_length"
        elif self.max_length:
            return "max_length"
        elif self.choices:
            return "choices"
        elif self.calc:
            return "calc"
        elif self.max_digits:
            return "max_digits"
        elif self.decimal_places:
            return "decimal_places"

    @property
    def value(self):
        """
        Returns the value of the property argument.
        """
        if self.unique:
            return self.unique_value
        elif self.readonly:
            return self.readonly_value
        elif self.required:
            return self.required_value
        elif self.min_length:
            return self.min_length_value
        elif self.max_length:
            return self.max_length_value
        elif self.choices:
            return self.choices_value
        elif self.calc:
            return self.calc_value
        elif self.max_digits:
            return self.max_digits_value
        elif self.decimal_places:
            return self.decimal_places_value


class ChoicesValue(object):

    """
    Python representation of choices value defined in grammar.
    """

    def __init__(self, parent, key, name):
        """
        Initialization of choices value.
        """
        super(ChoicesValue, self).__init__()

        self.parent = parent
        self.key = key
        self.name = name

    def __str__(self):
        return "(%s, %s)" % (self.key, self.name)


class CalculationValue(object):

    """
    Python representation of calculation value defined in grammar
    """

    def __init__(self, parent, first_operand, other_operands=None):
        """
        Initialization of calculation value
        """
        super(CalculationValue, self).__init__()
        self.first_operand = first_operand
        self.other_operands = other_operands if other_operands else []


class CalculationOperands(object):

    """
    Python representation of calculation operand defined in grammar
    """

    def __init__(self, operator, operand):
        """
        Initialization of calculation operand.
        """
        super(CalculationOperands, self).__init__()
        self.operator = operator
        self.operand = operand


class Action(object):

    """
    Python representation of action defined in grammar.
    """

    def __init__(self, parent, name, expression):
        super(Action, self).__init__()

        self.parent = parent
        self.name = name
        self.expression = expression

    def __str__(self):
        return self.name


class ActionExpression(object):

    """

    """

    def __init__(self, parent, first_operand, operator, second_operand):
        self.parent = parent
        self.first_operand = first_operand
        self.operator = operator
        self.second_operand = second_operand

# classes to instantiate via textX
_classes = (Model, Class, Property, PropertyArgument, ChoicesValue, Action,
            ActionExpression)

obj_processors = {
    "Model": model_processor,
    "Class": class_processor,
    "Property": property_processor,
    "Action": action_processor,
    "PropertyArgument": property_argument_processor,
}

_model_meta = None


def get_model_meta():
    """
    Gets model meta-model.
    """
    global _model_meta
    _model_meta = metamodel_from_file(os.path.join(os.path.dirname(__file__),
                                                   "model.tx"),
                                      classes=_classes)
    _model_meta.register_obj_processors(obj_processors)
    return _model_meta
