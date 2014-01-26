# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages


_version = "0.1.2"
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_short_description = "Python tool to find and list requirements of a Python project"


setup(
    name='requirements-detector',
    url='https://github.com/landscapeio/requirements-detector',
    author='landscape.io',
    author_email='code@landscape.io',
    description=_short_description,
    version=_version,
    scripts=['bin/detect-requirements'],
    install_requires=['astroid>=1.0.0'],
    packages=_packages,
    license='MIT',
    keywords='python requirements detector',
)
