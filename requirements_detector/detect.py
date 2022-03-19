import os
import re
import sys

from .exceptions import CouldNotParseRequirements, RequirementsNotFound
from .handle_setup import from_setup_py
from .requirement import DetectedRequirement

__all__ = [
    "find_requirements",
    "from_requirements_txt",
    "from_requirements_dir",
    "from_setup_py",
    "RequirementsNotFound",
    "CouldNotParseRequirements",
]


_PY3K = sys.version_info >= (3, 0)


_PIP_OPTIONS = (
    "-i",
    "--index-url",
    "--extra-index-url",
    "--no-index",
    "-f",
    "--find-links",
    "-r",
)


def find_requirements(path):
    """
    This method tries to determine the requirements of a particular project
    by inspecting the possible places that they could be defined.

    It will attempt, in order:

    1) to parse setup.py in the root for an install_requires value
    2) to read a requirements.txt file or a requirements.pip in the root
    3) to read all .txt files in a folder called 'requirements' in the root
    4) to read files matching "*requirements*.txt" and "*reqs*.txt" in the root,
       excluding any starting or ending with 'test'

    If one of these succeeds, then a list of pkg_resources.Requirement's
    will be returned. If none can be found, then a RequirementsNotFound
    will be raised
    """
    requirements = []

    setup_py = os.path.join(path, "setup.py")
    if os.path.exists(setup_py) and os.path.isfile(setup_py):
        try:
            requirements = from_setup_py(setup_py)
            requirements.sort()
            return requirements
        except CouldNotParseRequirements:
            pass

    for reqfile_name in ("requirements.txt", "requirements.pip"):
        reqfile_path = os.path.join(path, reqfile_name)
        if os.path.exists(reqfile_path) and os.path.isfile(reqfile_path):
            try:
                requirements += from_requirements_txt(reqfile_path)
            except CouldNotParseRequirements as e:
                pass

    requirements_dir = os.path.join(path, "requirements")
    if os.path.exists(requirements_dir) and os.path.isdir(requirements_dir):
        from_dir = from_requirements_dir(requirements_dir)
        if from_dir is not None:
            requirements += from_dir

    from_blob = from_requirements_blob(path)
    if from_blob is not None:
        requirements += from_blob

    requirements = list(set(requirements))
    if len(requirements) > 0:
        requirements.sort()
        return requirements

    raise RequirementsNotFound


def from_requirements_txt(requirements_file):
    # see http://www.pip-installer.org/en/latest/logic.html
    requirements = []
    with open(requirements_file) as f:
        for req in f.readlines():
            if req.strip() == "":
                # empty line
                continue
            if req.strip().startswith("#"):
                # this is a comment
                continue
            if req.strip().split()[0] in _PIP_OPTIONS:
                # this is a pip option
                continue
            detected = DetectedRequirement.parse(req, requirements_file)
            if detected is None:
                continue
            requirements.append(detected)

    return requirements


def from_requirements_dir(path):
    requirements = []
    for entry in os.listdir(path):
        filepath = os.path.join(path, entry)
        if not os.path.isfile(filepath):
            continue
        if entry.endswith(".txt") or entry.endswith(".pip"):
            # TODO: deal with duplicates
            requirements += from_requirements_txt(filepath)

    return requirements


def from_requirements_blob(path):
    requirements = []

    for entry in os.listdir(path):
        filepath = os.path.join(path, entry)
        if not os.path.isfile(filepath):
            continue
        m = re.match(r"^(\w*)req(uirement)?s(\w*)\.txt$", entry)
        if m is None:
            continue
        if m.group(1).startswith("test") or m.group(3).endswith("test"):
            continue
        requirements += from_requirements_txt(filepath)

    return requirements
