import os
from genodis.lang.meta import Model, get_model_meta
__author__ = 'Alen Suljkanovic'


def get_root_path():
    """
    Returns project's root path
    """
    path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    return path


def load_model(path):
    """
    Loads model from given path.
    """
    metamodel = get_model_meta()
    model = Model()
    for root, dirs, files in os.walk(path):
        for f in files:
            file_path = os.path.join(path, f)
            module = metamodel.model_from_file(file_path)
            module.name = f
            model.modules.append(module)

    return model
