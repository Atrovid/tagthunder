from glob import glob
from os.path import basename, join, dirname, splitext

from setuptools import find_packages, setup
import pathlib
import pkg_resources

# https://packaging.python.org/guides/single-sourcing-package-version/
# http://blog.ionelmc.ro/2014/05/25/python-packaging/

setup(
    name="tagthunder",
    version="0.0.1",
    author="François Ledoyen",
    author_email="francois.ledoyen@unicaen.fr",
    packages=["api", "pipeline"],
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
    install_requires=[
        "fastapi", "uvicorn", 
        "pydantic", "dacite", "email-validator",
        "requests", "urllib3",
        "beautifulsoup4", "lxml", "html5lib", 
        "numpy", "pandas", "sklearn", "pillow", "scipy", "matplotlib",
        "gtts", "langdetect", "googletrans==4.0.0-rc1", "pydub","librosa", "soundfile",
        "PyOpenAL",
        "yake", "inscriptis",
    ],
    entry_points={
        "console_scripts": [
            "run-api=api.main:run"
        ]
    }
)
