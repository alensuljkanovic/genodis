import os
from textx.metamodel import metamodel_from_file
from lang.meta import get_model_meta

__author__ = 'Alen Suljkanovic'

def test_simple_model():

    metamodel = get_model_meta()

    model_file = os.path.join("tests", "examples", "simple_model.tx")

    model = metamodel.model_from_file(model_file)

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
