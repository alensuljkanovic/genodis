__author__ = 'Alen Suljkanovic'


class CustomBaseException(Exception):
    """
    Base exception for all exceptions.
    """
    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message


class WrongPropertyArgument(Exception):
    """
    Raised in case argument is not allowed for given property type.
    """
    def __init__(self, argument, property):
        self.message = "Argument '%s' is not allowed for " \
                       "property type '%s'" % (argument, property.type)
