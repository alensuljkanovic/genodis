import os

__author__ = 'Alen Suljkanovic'


def get_root_path():
    """
    Returns project's root path
    """
    path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    return path
