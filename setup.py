# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import sys


_version = "0.5.1"
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

_short_description = "Python tool to find and list requirements of a Python project"

_CLASSIFIERS = (
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Topic :: Software Development :: Quality Assurance',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'License :: OSI Approved :: '
    'GNU General Public License v2 or later (GPLv2+)',
)


if sys.version_info < (2, 7):
    # pylint 1.4 dropped support for Python 2.6
    _install_requires = [
        'astroid>=1.0,<1.3.0',
    ]
else:
    _install_requires = [
        'astroid>=1.4',
    ]

setup(
    name='requirements-detector',
    url='https://github.com/landscapeio/requirements-detector',
    author='landscape.io',
    author_email='code@landscape.io',
    description=_short_description,
    version=_version,
    scripts=['bin/detect-requirements'],
    install_requires=_install_requires,
    packages=_packages,
    license='MIT',
    keywords='python requirements detector',
    classifiers=_CLASSIFIERS,
)
