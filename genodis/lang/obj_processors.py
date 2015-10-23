from .validators import TextValidator, DecimalValidator,\
    BaseValidator, CalculatedFieldValidator

__author__ = 'Alen Suljkanovic'


def choices_value_processor(choice_value):
    pass


def action_processor(action):
    """
    Action processor
    """
    pass


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
        if prop.type == "string" or prop.type == "choice":
            validator = TextValidator(prop)
        elif prop.type == "decimal":
            validator = DecimalValidator(prop)
        elif prop.type == "calculated_field":
            validator = CalculatedFieldValidator(prop)
        else:
            validator = BaseValidator(prop)

        validator.validate()

    if not hasattr(property, "django_field"):
        setattr(property, "django_field", None)

    django_mappings = {
        "string": "CharField",
        "text": "TextField",
        "int": "IntegerField",
        "float": "FloatField",
        "decimal": "DecimalField",
        "date": "DateField",
        "datetime": "DateTimeField",
        "choice": "CharField",
        "calculated_field": "DecimalField"
    }

    if property.type == "choice":
        choices = property.args_dict["choices"]
        # value for 'choices' argumet is string, so create list of tupples
        new_value = []
        for data in choices.value:
            new_value.append((data.key, data.name))

        # choices.value = tuple(new_value)
        # Dynamically add max length if it's not declared
        if "max_length" not in property.args_dict:
            from .meta import PropertyArgument
            arg = PropertyArgument(property, max_length=True,
                                   max_length_value=len(new_value))
            property.arguments.insert(0, arg)

    if property.type == "calculated_field":
        # if property argument 'decimal_places' is not set for calculated_field
        if "decimal_places" not in property.args_dict:
            from .meta import PropertyArgument
            arg = PropertyArgument(property, decimal_places=True,
                                   decimal_places_value=2)
            property.arguments.insert(0, arg)

    if property.type in django_mappings:
        property.django_field = django_mappings[property.type]

    _validate(property)


def property_argument_processor(prop_argument):
    """
    Property argument processor.
    """
    # If these property arguments are set in model, but their values are not
    # set, these values will have default value
    if prop_argument.unique and not prop_argument.unique_value:
        prop_argument.unique_value = True
    elif prop_argument.readonly and not prop_argument.readonly_value:
        prop_argument.readonly_value = True
    elif prop_argument.required and not prop_argument.required:
        prop_argument.required_value = True


def class_processor(_class):
    """
    Class processor
    """
    pass


def module_processor(module):
    """
    Model processor
    """
    pass
