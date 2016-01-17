"""
Util functions for genodis.
"""

import os
from lang.meta import Model, get_model_meta
from lang.exceptions import GenodisImportException,\
    GenodisClassNotDefinedException, GenodisClassRedefinitionException, \
    GenodisProjectException, GenodisContentImportException
from consts import ONE_TO_ONE, ONE_TO_MANY, MANY_TO_MANY,\
    MANY_TO_ONE, FOREIGN_KEY

import ConfigParser

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

        raise GenodisClassNotDefinedException(class_name)


    config_path = os.path.join(path, ".config")
    if not os.path.exists(config_path):
        raise GenodisProjectException(path)

    metamodel = get_model_meta()
    model = Model()

    config_parser = ConfigParser.ConfigParser()
    config_parser.read(os.path.join(path, ".config"))

    model.name = config_parser.get("app-data", "app_name")
    model.version = config_parser.get("app-data", "version")

    src_path = os.path.join(path, "src")
    for root, dirs, files in os.walk(src_path):
        for f in files:
            file_path = os.path.join(src_path, f)

            module = metamodel.model_from_file(file_path)
            module.name = f.replace(".gm", "")

            module_fqn = file_path.split(path)[1].replace(".gm", "")
            module.fqn = module_fqn[1:]
            model.modules[module.name] = module

    #
    # Resolving references
    #
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
                            raise GenodisImportException(_imp_module)
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
                                else:
                                    raise GenodisContentImportException(_import_obj.name, imp_obj)

                            content.imported_modules[_import_obj] = {
                                "classes": classes, "actions": actions
                            }
                    else:
                        raise GenodisImportException(selective.from_module)

        if content.classes:
            class_names = [c.name for c in module.content.classes]
            redefined = set([c for c in class_names
                             if class_names.count(c) > 1])
            if redefined:
                raise GenodisClassRedefinitionException(module.fqn,
                                                        list(redefined))

            for _class in content.classes:

                for prop in _class.references:
                    ref_class = content[prop.type]
                    if ref_class:
                        prop.type = ref_class
                    else:
                        ref_class = find_class_in_imports(
                            content.imported_modules,
                            prop.type
                        )
                        prop.type = ref_class

                    if ref_class.references:
                        for ref_prop in ref_class.references:
                            if ref_prop.type == _class:
                                if prop.list and ref_prop.list:
                                    _class.add_relationship(MANY_TO_MANY, prop,
                                                            ref_class)
                                    #ref_class.add_relationship(MANY_TO_MANY,
                                    #                           ref_prop,
                                    #                           _class)
                                elif prop.list and not ref_prop.list:
                                    _class.add_relationship(ONE_TO_MANY, prop,
                                                            ref_class)
                                    #ref_class.add_relationship(MANY_TO_ONE,
                                    #                           ref_prop,
                                    #                           _class)
                                elif not prop.list and ref_prop.list:
                                    _class.add_relationship(MANY_TO_ONE, prop,
                                                            ref_class)
                                    #ref_class.add_relationship(ONE_TO_MANY, _class)
                                else:
                                    _class.add_relationship(ONE_TO_ONE, ref_class)
                                    # ref_class.add_relationship(ONE_TO_ONE, _class)
                    else:
                        if prop.list:
                            _class.add_relationship(ONE_TO_MANY, prop, ref_class)
                            ref_class.add_relationship(MANY_TO_ONE,
                                                       _class.name.lower(),
                                                       _class)
                        else:
                            _class.add_relationship(FOREIGN_KEY, prop, ref_class)

                print(_class.name)
                for ref in _class.relationships:
                    name = ref if isinstance(ref, unicode) else ref.name
                    print("Prop %s" % name)
                    ref_lst = _class.relationships[ref]
                    for ref_data in ref_lst:
                        print("\t rel %s" % ref_data[0])
                        print("\t rel %s" % ref_data[1])
    return model
