#!/usr/bin/env python

from glob import glob
from os.path import basename, join, dirname, splitext

from setuptools import find_packages, setup
import pathlib
import pkg_resources

# https://packaging.python.org/guides/single-sourcing-package-version/
# http://blog.ionelmc.ro/2014/05/25/python-packaging/

_PATH_ROOT = dirname(__file__)
_PATH_REQUIRE = join(_PATH_ROOT, "requirements.txt")

with pathlib.Path(_PATH_REQUIRE).open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="tagthunder",
    version="0.0.1",
    author="François Ledoyen",
    author_email="francois.ledoyen@unicaen.fr",
    packages=["api", "algorithms"],
    package_dir={"": "tagthunder"},
    include_package_data=False,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python :: 3.9",
        "Operating System :: Unixr",
    ],
    python_requires=">=3.9",
    setup_requires=[],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "run-api=api.main:run"
        ]
    }
)
