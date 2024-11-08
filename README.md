# Requirements Detector

## Status

[![Latest Version](https://img.shields.io/pypi/v/requirements-detector.svg?label=version&style=flat)](https://pypi.python.org/pypi/requirements-detector)
[![Build Satus](https://github.com/landscapeio/requirements-detector/actions/workflows/ci.yaml/badge.svg)](https://github.com/landscapeio/requirements-detector/actions/workflows/ci.yaml)
[![Health](https://landscape.io/github/landscapeio/requirements-detector/master/landscape.svg?style=flat)](https://landscape.io/github/landscapeio/requirements-detector/master)
[![Coverage Status](https://img.shields.io/coveralls/landscapeio/requirements-detector.svg?style=flat)](https://coveralls.io/r/landscapeio/requirements-detector)
[![Documentation](https://readthedocs.org/projects/requirements-detector/badge/?version=master)](https://readthedocs.org/projects/requirements-detector/)

## About

`requirements-detector` is a simple Python tool which attempts to find and list the requirements of a Python project.

When run from the root of a Python project, it will try to ascertain which libraries and the versions of those libraries that the project depends on.

It uses the following methods in order, in the root of the project:

1. Parse `setup.py` (if this is successful, the remaining steps are skipped)
2. Parse `pyproject.toml` (if a `tool.poetry.dependencies` section is found, the remaining steps are skipped)
3. Parse `requirements.txt` or `requirements.pip`
4. Parse all `*.txt` and `*.pip` files inside a folder called `requirements`
5. Parse all files in the root folder matching `*requirements*.txt` or `reqs.txt` (so for example, `pip_requirements.txt` would match, as would `requirements_common.txt`)

### Usage

```
detect-requirements [path]
```
If `path` is not specified, the current working directory will be used.

### Output

The output will be plaintext, and match that of a [pip requirements file](http://www.pip-installer.org/en/latest/logic.html), for example:

```
Django==1.5.2
South>=0.8
anyjson
celery>=2.2,<3
```

### Usage From Python

```
>>> import os
>>> from requirements_detector import find_requirements
>>> find_requirements(os.getcwd())
[DetectedRequirement:Django==1.5.2, DetectedRequirement:South>=0.8, ...]
```


If you know the relevant file or directory,  you can use `from_requirements_txt`, `from_setup_py` or `from_requirements_dir` directly.

```
>>> from requirements_detector import from_requirements_txt
>>> from_requirements_txt("/path/to/requirements.txt")
[DetectedRequirement:Django==1.5.2, DetectedRequirement:South>=0.8, ...]
```
