#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup

__author__ = "Alen"
__version__ = "0.1"

NAME = 'genodis'
DESC = 'Language for web app development'
VERSION = __version__
AUTHOR = 'Alen'
AUTHOR_EMAIL = 'igor DOT dejanovic AT gmail DOT com'
LICENSE = 'MIT'
URL = 'https://github.com/igordejanovic/textX'
DOWNLOAD_URL = 'https://github.com/igordejanovic/textX/archive/v%s.tar.gz' % VERSION
#README = codecs.open(os.path.join(os.path.dirname(__file__), 'README.rst'),
#                     'r', encoding='utf-8').read()
README = "Citaj me"

setup(
    name = NAME,
    version = VERSION,
    description = DESC,
    long_description = README,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,
    license = LICENSE,
    url = URL,
    download_url = DOWNLOAD_URL,
    packages = ["genodis"],
    install_requires = ["textx", "jinja2"],
    keywords = "parser meta-language meta-model language DSL",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]

)
