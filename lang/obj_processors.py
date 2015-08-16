__author__ = 'Alen Suljkanovic'


def action_processor(action):
    """
    Action processor
    """
    print(str(action.expression.second_operand.first_operand.name))


def property_processor(property):
    """
    Property processor
    """
    # print(property)
    pass


def class_processor(_class):
    """
    Class processor
    """
    # print(_class)
    pass


def model_processor(model):
    """
    Model processor
    """
    pass
