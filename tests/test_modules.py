from genodis.utils import load_model

__author__ = 'Alen Suljkanovic'


def test_simple_model():

    model = load_model("/home/biohazard1491/genodis/tests/examples/modules")
    for module in model.modules.values():
        print(module.name)

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
