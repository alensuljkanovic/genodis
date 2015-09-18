import os
import jinja2
from genodis.lang.meta import get_model_meta
from genodis.consts import TEMPLATES_PATH, SRC_GEN_PATH

__author__ = 'Alen Suljkanovic'


class BaseGenerator(object):
    """
    Base generator which is inherited by all other generators.
    """
    def __init__(self, model):
        super(BaseGenerator, self).__init__()
        self.model = model

    @staticmethod
    def create_init_file(path_to_file):
        """
        Create __init__.py file at given path.
        """
        init_path = os.path.join(path_to_file, "__init__.py")
        with open(init_path, "w") as f:
            f.write("")

    @staticmethod
    def setup_env():
        root_path = os.path.dirname(__file__).replace("genodis", "")
        templates_path = os.path.join(root_path, TEMPLATES_PATH)

        file_loader = jinja2.FileSystemLoader(templates_path)

        jinja_env = jinja2.Environment(loader=file_loader)
        return jinja_env

    def generate(self):
        """
        Generates code.
        """
        raise Exception("Not implemented!")


class DjangoServerGenerator(BaseGenerator):
    """
    Generates django server.
    """
    def __init__(self, model):
        super(DjangoServerGenerator, self).__init__(model)

    def generate(self):
        root_path = os.path.dirname(__file__).replace("genodis", "")
        jinja_env = self.setup_env()

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


class AngularJSGenerator(BaseGenerator):
    """
    Generates AngularJS client app.
    """
    def __init__(self, model):
        super(AngularJSGenerator, self).__init__(model)

    def generate(self):
        root_path = os.path.dirname(__file__).replace("src", "")
        jinja_env = self.setup_env()

        d = {"model": self.model, "app_name": self.model.name.lower()}

        destination = os.path.join(root_path, SRC_GEN_PATH)

        if not os.path.exists(destination):
            os.mkdir(destination)

        angular_app_name = self.model.name.lower() + "_js"
        angular_path = os.path.join(destination, angular_app_name)
        os.mkdir(angular_path)

        # create app folder
        angular_app = os.path.join(angular_path, "app")
        os.mkdir(angular_app)


        #
        # Create app.js
        #
        template = jinja_env.get_template("angularjs/app.template")
        template.stream(d).dump(os.path.join(angular_app, 'app.js'))

        #
        # Create app.css
        #
        template = jinja_env.get_template("angularjs/app_css.template")
        template.stream(d).dump(os.path.join(angular_app, 'app.css'))

        #
        # Create index.html
        #
        template = jinja_env.get_template("angularjs/index.template")
        template.stream(d).dump(os.path.join(angular_app, 'index.html'))

        # create controllers folder
        controllers_path = os.path.join(angular_app, "controllers")
        os.mkdir(controllers_path)
        #
        # Create controllers for all classes
        #
        template = jinja_env.get_template("angularjs/controllers.template")
        for c in self.model.classes:
            ctlr_name = c.name.lower() + "_controller.js"
            data = {"c": c}
            template.stream(data).dump(os.path.join(controllers_path, ctlr_name))

        # create views folder
        views_path = os.path.join(angular_app, "views")
        os.mkdir(views_path)
        #
        # Create views for all classes
        #
        template = jinja_env.get_template("angularjs/views.template")
        for c in self.model.classes:
            view_name = c.name.lower() + "s.html"
            data = {"c": c}
            template.stream(data).dump(os.path.join(views_path, view_name))


if __name__ == "__main__":
    metamodel = get_model_meta()

    path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    model_file = os.path.join(path, "tests", "examples", "simple_model.tx")
    model = metamodel.model_from_file(model_file)

    server_generator = DjangoServerGenerator(model)
    server_generator.generate()

    angular_generator = AngularJSGenerator(model)
    angular_generator.generate()
