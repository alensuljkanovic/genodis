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

    def __init__(self, _type="decimal"):
        self.message = "Type '%s' must contain argument 'decimal_places'" % \
            _type


class GenodisImportError(CustomBaseException):

    def __init__(self, _import):
        self.message = "No module named %s" % _import


class GenodisClassImportError(CustomBaseException):

    def __init__(self, module_name, class_name):
        self.message = "Cannot import class %s. The class doesn't exist in \
                       the module %s" (class_name, module_name)


class GenodisClassNotDefined(CustomBaseException):

    def __init__(self, class_name):
        self.message = "Class %s is not defined." % class_name


class GenodisClassRedefinitionException(CustomBaseException):

    def __init__(self, module, classes):
        if len(classes) == 1:
            self.message = "Redefinition of class '%s' in module '%s'" % \
                (classes[0], module)
        else:
            class_names = ""
            for i, c in enumerate(class_names):
                class_names += "'%s'" % c
                if i == len(class_names) - 1:
                    class_names += "and '%s'" % c
                else:
                    class_names += ","
            self.message = "Redefinition of classes %s in module '%s'" % \
                (class_names, module)
