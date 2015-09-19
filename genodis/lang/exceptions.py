__author__ = 'Alen Suljkanovic'


class CustomBaseException(Exception):
    """
    Base exception for all exceptions.
    """
    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message


class InvalidPropertyArgument(CustomBaseException):
    """
    Raised in case argument is not allowed for given property type.
    """
    def __init__(self, argument, property):
        self.message = "Argument '%s' is not allowed for " \
                       "property type '%s'." % (argument.name, property.type)


class InvalidPropertyArgValue(CustomBaseException):
    """
    Raised in case value for property argument is invalid.
    """
    def __init__(self, argument):
        self.message = "Invalid value '%s' for property argument '%s'." % (
            argument.value, argument.name
        )


class InvalidDefaultArgValue(CustomBaseException):
    """
    Raised when default has incorrect value.
    """
    def __init__(self, argument, prop):
        self.message = "Invalid default value '%s' for property type '%s'." % (
            argument.value, prop.type
        )


class DecimalArgsException(CustomBaseException):

    def __init__(self):
        self.message = "Type 'decimal' must contain argument 'decimal_places'"