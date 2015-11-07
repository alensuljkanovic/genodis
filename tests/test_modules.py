from genodis.utils import load_model, get_root_path
from genodis.generator import DjangoServerGenerator, AngularJSGenerator
import os

__author__ = 'Alen Suljkanovic'


def test_simple_model():

    path = os.path.join(get_root_path(), "tests", "examples",
                        "modules_example")

    model = load_model(path)

    server_generator = DjangoServerGenerator(model)
    server_generator.generate()

    angular_generator = AngularJSGenerator(model, generate_as_static=True)
    angular_generator.generate()
