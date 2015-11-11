__author__ = 'Alen Suljkanovic'


class CustomBaseException(Exception):

    """
    Base exception for all exceptions.
    """

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message


class InvalidPropertyArgumentException(CustomBaseException):

    """
    Raised in case argument is not allowed for the given property type.
    """

    def __init__(self, argument, property):
        self.message = "Argument '%s' is not allowed for " \
                       "property type '%s'." % (argument.name, property.type)


class InvalidPropertyArgValueException(CustomBaseException):

    """
    Raised in case value for the property argument is invalid.
    """

    def __init__(self, argument):
        self.message = "Invalid value '%s' for property argument '%s'." % (
            argument.value, argument.name
        )


class InvalidDefaultArgValueException(CustomBaseException):

    """
    Raised when the default has incorrect value.
    """

    def __init__(self, argument, prop):
        self.message = "Invalid default value '%s' for property type '%s'." % (
            argument.value, prop.type
        )


class DecimalArgsException(CustomBaseException):

    def __init__(self, _type="decimal"):
        self.message = "Type '%s' must contain argument 'decimal_places'" % \
            _type

class GenodisProjectException(CustomBaseException):
    """
    Raised when trying to load the project which does not contain .config file.
    """

    def __init__(self, path):
        self.message = "Couldn't find Genodis project at given path: %s." % \
            path


class GenodisImportException(CustomBaseException):
    """
    Raised when trying to import unexisting module.
    """
    def __init__(self, _import):
        self.message = "No module named %s" % _import


class GenodisContentImportException(CustomBaseException):
    """
    Raised when trying to import unexisting class or action.
    """
    def __init__(self, module_name, class_name):
        self.message = "Cannot import class or action '%s'. It doesn't exist in \
                       the module %s"  % (class_name, module_name)


class GenodisClassNotDefinedException(CustomBaseException):
    """
    Raised when referencing the unexisting class from property type.
    """
    def __init__(self, class_name):
        self.message = "Class %s is not defined." % class_name


class GenodisClassRedefinitionException(CustomBaseException):
    """
    Raised when the class is redefined inside the module.
    """

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
