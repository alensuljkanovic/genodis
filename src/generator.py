import os
import jinja2
from jinja2.environment import Environment
from lang.meta import get_model_meta
from src.consts import TEMPLATES_PATH, DJANGO_TEMPLATES, SRC_GEN_PATH, \
    DJANGO_DESTINATION

__author__ = 'Alen Suljkanovic'


class Generator(object):
    """
    Class that represents code generator for server and client.
    """
    def __init__(self, model):
        self.model = model

    @staticmethod
    def create_init_file(path_to_file):
        """
        Create __init__.py file at given path.
        """
        init_path = os.path.join(path_to_file, "__init__.py")
        with open(init_path, "w") as f:
            f.write("")

    def generate(self):

        root_path = os.path.dirname(__file__).replace("src", "")
        templates_path = os.path.join(root_path, TEMPLATES_PATH)

        file_loader = jinja2.FileSystemLoader(templates_path)

        jinja_env = jinja2.Environment(loader=file_loader)

        template = jinja_env.get_template("main.template")

        d = {"model": self.model, "app_name": self.model.name.lower()}

        destination = os.path.join(root_path, SRC_GEN_PATH)

        if not os.path.exists(destination):
            os.mkdir(destination)

            django_path = os.path.join(destination, self.model.name.lower())
            os.mkdir(django_path)

            #
            # Create manage.py file
            #
            template = jinja_env.get_template("django/django_manage.template")
            template.stream(d).dump(os.path.join(django_path, 'manage.py'))

            #
            # Create folder with settings.py, urls.py and wsgi.py
            #
            app_settings = os.path.join(django_path, model.name.lower())
            os.mkdir(app_settings)
            self.create_init_file(app_settings)

            template = jinja_env.get_template("django/django_settings.template")
            template.stream(d).dump(os.path.join(app_settings, 'settings.py'))

            template = jinja_env.get_template("django/django_urls.template")
            template.stream(d).dump(os.path.join(app_settings, 'urls.py'))

            template = jinja_env.get_template("django/django_wsgi.template")
            template.stream(d).dump(os.path.join(app_settings, 'wsgi.py'))

            #
            # Create app folder
            #
            django_app = os.path.join(django_path, model.name.lower() + "_app")
            os.mkdir(django_app)
            self.create_init_file(django_app)

            #
            # Creating admin.py file
            #
            template = jinja_env.get_template("django/django_admin.template")
            template.stream(d).dump(os.path.join(django_app, 'admin.py'))

            #
            # Creating models.py file
            #
            template = jinja_env.get_template("django/django_models.template")
            template.stream(d).dump(os.path.join(django_app, 'models.py'))

            #
            # Creating tests.py file
            #
            template = jinja_env.get_template("django/django_tests.template")
            template.stream(d).dump(os.path.join(django_app, 'tests.py'))

            #
            # Creating urls.py file
            #
            template = jinja_env.get_template("django/django_urls.template")
            template.stream(d).dump(os.path.join(django_app, 'urls.py'))

            #
            # Creating views.py file
            #
            template = jinja_env.get_template("django/django_views.template")
            template.stream(d).dump(os.path.join(django_app, 'views.py'))


            # creating folder for migrations
            migrations_path = os.path.join(django_app, "migrations")
            os.mkdir(migrations_path)
            self.create_init_file(migrations_path)

            # creating folder for templates
            templates_path = os.path.join(django_app, "templates")
            os.mkdir(templates_path)

            view_templates = os.path.join(templates_path,
                                          self.model.name.lower())
            os.mkdir(view_templates)


if __name__ == "__main__":
    metamodel = get_model_meta()

    path = os.path.dirname(__file__).replace("src", "")
    model_file = os.path.join(path, "tests", "examples", "simple_model.tx")
    model = metamodel.model_from_file(model_file)

    generator = Generator(model)
    generator.generate()