from .exceptions import InvalidPropertyArgValueException, \
    InvalidPropertyArgumentException, InvalidDefaultArgValueException, \
    DecimalArgsException

__author__ = 'Alen Suljkanovic'


class BaseValidator(object):

    """
    Base class for all validators.
    """

    def __init__(self, prop):
        super(BaseValidator, self).__init__()
        self.prop = prop

        # Dictionary where name of the allowed args are keys, and
        # the values are tupples of allowed values.
        self._allowed_args = {
            "blank": ("", True, False),
            "default": [None],
            "editable": ("", True, False),
            "unique": ("", True, False),
            "readonly": ("", True, False),
            "required": ("", True, False)
        }

        self.numbers = ["int", "float", "decimal"]

    def validate(self):
        """
        Validate property.
        """
        for arg in self.prop.arguments:
            if arg.name in self.allowed_arguments:

                if arg.name == "calc":
                    continue

                valid_data = self.allowed_arguments[arg.name]
                valid = False

                if valid_data in self.numbers:
                    # If argument value must be number, check if the set value
                    # is correct.
                    try:
                        if valid_data == "int":
                            int(arg.value)
                        elif valid_data == "float" or valid_data == "decimal":
                            float(arg.value)
                        valid = True
                    except:
                        pass
                elif arg.name == "default":
                    # default value depends on property type, so we need to
                    # handle this argument separately.
                    print("DEFAULT %s" % arg.value)
                    try:
                        if self.prop.type == "int":
                            int(arg.value)
                        elif self.prop.type in ["float", "decimal"]:
                            float(arg.value)
                        valid = True
                    except:
                        raise InvalidDefaultArgValueException(arg, self.prop)
                elif arg.name == "choices":
                    # FIXME check if value is in correct format!
                    if arg.value:
                        valid = True
                else:
                    if arg.value in valid_data:
                        valid = True

                if not valid:
                    raise InvalidPropertyArgValueException(arg)
            else:
                raise InvalidPropertyArgumentException(arg, self.prop)

    @property
    def allowed_arguments(self):
        """
        Returns dictionary with all allowed arguments for given property.
        """
        return self._allowed_args


class TextValidator(BaseValidator):

    def __init__(self, prop):
        super(TextValidator, self).__init__(prop)

    @property
    def allowed_arguments(self):
        self._allowed_args["max_length"] = "int"
        self._allowed_args["choices"] = ""
        return self._allowed_args


class DecimalValidator(BaseValidator):

    def __init__(self, prop):
        super(DecimalValidator, self).__init__(prop)

    @property
    def allowed_arguments(self):
        self._allowed_args["max_digits"] = "int"
        self._allowed_args["decimal_places"] = "int"
        return self._allowed_args

    def validate(self):
        super(DecimalValidator, self).validate()

        max_digits_exits = False
        dec_places_exits = False
        for arg in self.prop.arguments:
            if arg.name == "max_digits":
                max_digits_exits = True
            elif arg.name == "decimal_places":
                dec_places_exits = True

        if max_digits_exits and not dec_places_exits:
            raise DecimalArgsException()


class CalculatedFieldValidator(BaseValidator):

    """
    Validator for the calculated field
    """

    def __init__(self, prop):
        super(CalculatedFieldValidator, self).__init__(prop)

    @property
    def allowed_arguments(self):
        self._allowed_args.clear()
        self._allowed_args["max_digits"] = "int"
        self._allowed_args["decimal_places"] = "int"
        self._allowed_args["unique"] = ("", True, False)
        self._allowed_args["calc"] = ""  # calc can contain anything
        return self._allowed_args

    def validate(self):
        super(CalculatedFieldValidator, self).validate()

        max_digits_exits = False
        dec_places_exits = False
        for arg in self.prop.arguments:
            if arg.name == "max_digits":
                max_digits_exits = True
            elif arg.name == "decimal_places":
                dec_places_exits = True

        if max_digits_exits and not dec_places_exits:
            raise DecimalArgsException(_type="calculated_field")
