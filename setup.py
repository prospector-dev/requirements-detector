# -*- coding: UTF-8 -*-
import sys
from distutils.core import setup

from setuptools import find_packages

if sys.version_info < (2, 7):
    # pylint 1.4 dropped support for Python 2.6
    _install_requires = [
        "astroid>=1.0,<1.3.0",
    ]
elif sys.version_info < (3, 0):
    # astroid 2.x is Python 3 only
    _install_requires = [
        "astroid>=1.4,<2.0",
    ]
else:
    _install_requires = [
        "astroid>=1.4",
    ]

setup(
    scripts=["bin/detect-requirements"],
    install_requires=_install_requires,
)
