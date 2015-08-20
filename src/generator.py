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

    def generate(self):

        root_path = os.path.dirname(__file__).replace("src", "")
        templates_path = os.path.join(root_path, TEMPLATES_PATH)

        file_loader = jinja2.FileSystemLoader(templates_path)

        jinja_env = jinja2.Environment(loader=file_loader)

        template = jinja_env.get_template("main.template")

        d = {"model": self.model}

        destination = os.path.join(root_path, SRC_GEN_PATH)

        if not os.path.exists(destination):
            os.mkdir(destination)

            django_path = os.path.join(destination, DJANGO_DESTINATION)
            os.mkdir(django_path)

            django_app = os.path.join(django_path, model.name)
            os.mkdir(django_app)

            template = jinja_env.get_template("django/django_settings.template")
            template.stream(d).dump(os.path.join(django_app, 'settings.py'))

            template = jinja_env.get_template("django/django_urls.template")
            template.stream(d).dump(os.path.join(django_app, 'urls.py'))

            template = jinja_env.get_template("django/django_wsgi.template")
            template.stream(d).dump(os.path.join(django_app, 'wsgi.py'))



if __name__ == "__main__":
    metamodel = get_model_meta()

    path = os.path.dirname(__file__).replace("src", "")
    model_file = os.path.join(path, "tests", "examples", "simple_model.tx")
    model = metamodel.model_from_file(model_file)

    generator = Generator(model)
    generator.generate()