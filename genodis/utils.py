import os
from genodis.lang.meta import Model, get_model_meta
from genodis.lang.exceptions import GenodisImportError, GenodisClassNotDefined
import configparser

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
    def find_class_in_imports(imported_modules, class_name):
        """
        Returns class from imports declared in module, if found.
        """

        for module in imported_modules:
            content = module.content

            imported_objects = imported_modules[module]
            if imported_objects == "*":
                _class = content[class_name]
                if _class:
                    return _class

            elif "classes" in imported_objects:
                for _class in imported_objects["classes"]:
                    if _class.name == class_name:
                        return _class

        raise GenodisClassNotDefined(class_name)

    metamodel = get_model_meta()
    model = Model()
    config_parser = configparser.ConfigParser()
    config_parser.read(os.path.join(path, ".config"))

    model.name = config_parser["app-data"]["app_name"]
    model.version = config_parser["app-data"]["version"]

    src_path = os.path.join(path, "src")
    for root, dirs, files in os.walk(src_path):
        for f in files:
            file_path = os.path.join(src_path, f)
            module = metamodel.model_from_file(file_path)
            module.name = f.replace(".gm", "")
            model.modules[module.name] = module

    # resolving references
    for module in model.modules.values():
        content = module.content
        if content.imports:
            for _import in content.imports[:]:
                if _import.module:
                    for _imp_module in _import.module.modules:
                        if _imp_module in model.modules:
                            _import_obj = model.modules[_imp_module]
                            # Replace string with module object
                            index = content.imports.index(_import)
                            content.imports[index] = _import_obj
                            content.imported_modules[_import_obj] = "*"
                        else:
                            raise GenodisImportError(_imp_module)
                if _import.selective:
                    selective = _import.selective
                    if selective.from_module in model.modules:
                        _import_obj = model.modules[selective.from_module]
                        index = content.imports.index(_import)
                        content.imports[index] = _import_obj
                        # in case of: from module_name import *
                        if selective.selector.value[0] == "*":
                            content.imported_modules[_import_obj] = "*"
                        else:  # go through imported objects and add into lists
                            classes = []
                            actions = []
                            im_content = _import_obj.content

                            for imp_obj in selective.selector.value:
                                # if class is in module
                                # TODO import actions
                                if imp_obj in _import_obj.content:
                                    classes.append(im_content[imp_obj])

                            content.imported_modules[_import_obj] = {
                                "classes": classes, "actions": actions
                            }
                    else:
                        raise GenodisImportError(selective.from_module)

        if content.classes:
            for _class in content.classes:
                for prop in _class.references:
                    local_class = content[prop.type]
                    if local_class:
                        prop.type = local_class
                    else:
                        find_class_in_imports(content.imported_modules,
                                              prop.type)

    return model
