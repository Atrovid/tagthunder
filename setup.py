#!/usr/bin/env python

from glob import glob
from os.path import basename, join, dirname, splitext
from pip.req import parse_requirements

from setuptools import find_packages, setup

# https://packaging.python.org/guides/single-sourcing-package-version/
# http://blog.ionelmc.ro/2014/05/25/python-packaging/

_PATH_ROOT = dirname(__file__)
_PATH_REQUIRE = join(_PATH_ROOT, "requirements.txt")

setup(
    name="tagthunder",
    version="0.0.1",
    author="François Ledoyen",
    author_email="francois.ledoyen@unicaen.fr",
    packages=find_packages("tagthunder"),
    package_dir={"":"tagthunder"},
    py_modules=[splitext(path)[0] for path in glob('tagthunder/*.py')],
    include_package_data=False,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unixr",
    ],
    python_requires=">=3.9",
    setup_requires=[],
    install_requires=[str(ir.req) for ir in parse_requirements(_PATH_REQUIRE)],
    entry_points={
        "console_scripts" : [
zsh:1: command not found: q
        ]
    }
)
