# Requirements Detector


`requirements-detector` is a simple Python tool which attempts to find and list the requirements of a Python project. 

When run from the root of a Python project, it will try to ascertain which libraries and the versions of those libraries that the project depends on.

It uses the following methods in order, in the root of the project:

1. Parse `setup.py`
2. Parse `requirements.txt`
3. Parse all `*.txt` files inside a folder called `requirements`
4. Parse all files in the root folder matching `*requirements*.txt` or `reqs.txt` (so for example, `pip_requirements.txt` would match, as would `requirements_common.txt`)

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