import os
from textx.metamodel import metamodel_from_file
from genodis.lang.obj_processors import model_processor, class_processor, \
    property_processor, action_processor, property_argument_processor, \
    choices_value_processor

__author__ = 'Alen Suljkanovic'


class Model(object):
    """
    Python representation of model defined in grammar.
    """

    def __init__(self, name, classes, actions=None, bindings=None):
        """
        Initialization of model
        """
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
                 choices=None, choices_value=None):
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
        self._value = None

    def __str__(self):
        if self.required:
            return "blank=%s" % self.value
        elif not self.choices:
            return "%s=%s" % (self.name, self.value)
        else:
            ret = tuple((data.key, data.name) for data in self.choices_value)
            return "%s=%s" %(self.name, ret)

    @property
    def name(self):
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

    @property
    def value(self):
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


class ChoicesValue(object):
    """
    Python representation of choices value defined in grammar.
    """
    def __init__(self, parent, key, name):
        self.parent = parent
        self.key = key
        self.name = name

    def __str__(self):
        return "(%s, %s)" % (self.key, self.name)


class Action(object):
    """
    Python representation of action defined in grammar.
    """
    def __init__(self, parent, name, expression):
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
