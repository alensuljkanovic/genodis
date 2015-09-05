from lang.validators import TextValidator, DecimalValidator, BaseValidator

__author__ = 'Alen Suljkanovic'


def action_processor(action):
    """
    Action processor
    """
    print(str(action.expression.second_operand.first_operand.name))


def property_processor(property):
    """
    Property processor
    """
    def resolve_date(args):
        for arg in args:
            if arg.name == "format":
                print("format value %s" % arg.value)

    def _validate(prop):
        validator = None
        if prop.type == "string":
            validator = TextValidator(prop)
        elif prop.type == "decimal":
            validator = DecimalValidator(prop)
        else:
            validator = BaseValidator(prop)

        validator.validate()

    _validate(property)

    if not hasattr(property, "django_field"):
        setattr(property, "django_field", None)

    django_mappings = {
        "string": "CharField",
        "text": "TextField",
        "int": "IntegerField",
        "float": "FloatField",
        "decimal": "DecimalField",
        "date": "DateField",
        "datetime": "DateTimeField"
    }

    if property.type in django_mappings:
        property.django_field = django_mappings[property.type]


def property_argument_processor(prop_argument):
    """
    Property argument processor.
    """
    if prop_argument.name == "unique":
        if not prop_argument.value:
            prop_argument.value = True


def class_processor(_class):
    """
    Class processor
    """
    # print(_class)
    pass


def model_processor(model):
    """
    Model processor
    """
    # Dictionary of all classes in model
    all_classes = {c.name: c for c in model.classes}

    for c in model.classes:
        for p in c.properties:
            if p.type in all_classes and not c.session:
                if p.list:
                    ref_class = all_classes[p.type]
                    ref_class.foreign_key = c