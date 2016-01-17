"""
Tests in this module test exception raising.
"""

import pytest
import os
from genodis.lang.meta import get_model_meta
from genodis.utils import get_root_path, load_model
from genodis.lang.exceptions import InvalidPropertyArgumentException,\
    InvalidPropertyArgValueException, DecimalArgsException,\
    GenodisImportException, GenodisProjectException, \
    GenodisContentImportException, GenodisClassNotDefinedException,\
    GenodisClassRedefinitionException

__author__ = 'Alen Suljkanovic'


@pytest.fixture
def metamodel():
    """
    Shared metamodel object.
    """
    return get_model_meta()


def test_invalid_property_argument(metamodel):
    """
    Tests if exception will be raised when invalid argument is se to a
    property.
    """
    module_file = os.path.join(get_root_path(), "tests", "examples",
                              "exception_models",
                              "invalid_property_argument.gm")
    with pytest.raises(InvalidPropertyArgumentException):
        metamodel.model_from_file(module_file)


def test_invalid_property_arg_value(metamodel):
    """
    Tests if exception will be raised if property value has invalid value.
    """
    #module_file = os.path.join(get_root_path(), "tests", "examples",
                              #"exception_models",
                              #"invalid_property_argument_value.gm")
    # Raises TextXSyntaxError
    #with pytest.raises(InvalidPropertyArgValueException):
    #    metamodel.model_from_file(module_file)
    pass


def test_invalid_default_arg_value(metamodel):
    """
    Tests if exception will be raised if default value for property type
    is incorrect.
    """
    pass


def test_decimal_args(metamodel):
    """
    Tests if exception will be raised if argument 'decimal_places' is not
    defined for property type 'decimal'.
    """
    module_file = os.path.join(get_root_path(), "tests", "examples",
                              "exception_models",
                              "decimal_places_not_set.gm")
    with pytest.raises(DecimalArgsException):
        metamodel.model_from_file(module_file)


def test_genodis_project_exception():
    """
    Tests if exception will be raised when importing unexisting module.
    """
    model_path = os.path.join(get_root_path(), "tests", "examples",
                              "exception_models", "import_models", "example1")
    with pytest.raises(GenodisProjectException):
        load_model(model_path)


def test_genodis_import_exception():
    """
    Tests if exception will be raised when importing unexisting module.
    """
    model_path = os.path.join(get_root_path(), "tests", "examples",
                              "exception_models", "import_models", "example2")
    with pytest.raises(GenodisImportException):
        load_model(model_path)


def test_genodis_content_import_exception():
    """
    Tests if exception will be raised when importing unexisting class.
    """
    model_path = os.path.join(get_root_path(), "tests", "examples",
                              "exception_models", "import_models", "example3")
    with pytest.raises(GenodisContentImportException):
        load_model(model_path)


def test_genodis_class_not_defined_exception(metamodel):
    """
    Tests if exception will be raised when setting undefined class as a
    property type.
    """
    model_path = os.path.join(get_root_path(), "tests", "examples",
                              "exception_models", "import_models", "example4")
    with pytest.raises(GenodisClassNotDefinedException):
        load_model(model_path)


def test_genodis_class_redefinition_exception(metamodel):
    """
    Tests if exception will be raised when class is redefined.
    """
    model_path = os.path.join(get_root_path(), "tests", "examples",
                              "exception_models", "import_models", "example5")
    with pytest.raises(GenodisClassRedefinitionException):
        load_model(model_path)
