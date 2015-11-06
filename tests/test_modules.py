from genodis.utils import load_model, get_root_path
from genodis.generator import DjangoServerGenerator, AngularJSGenerator
import os

__author__ = 'Alen Suljkanovic'


def test_simple_model():

    path = os.path.join(get_root_path(), "tests", "examples",
                        "modules_example")
    print("PATH %s" % path)
    model = load_model(path)

    server_generator = DjangoServerGenerator(model)
    server_generator.generate()

    angular_generator = AngularJSGenerator(model, generate_as_static=True)
    angular_generator.generate()
    # assert model.name == "Supermarket"
    # assert len(model.entities) == 3
    #
    # person = model.entities[0]
    # assert len(person.properties) == 3
    #
    # first_name = person.properties[0]
    # assert first_name.name == "first_name"
    # assert first_name.type == "string"
    #
    # for p in person.properties:
    #     print(p)
