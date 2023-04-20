import re
from pathlib import Path
from typing import List, Union

import toml

from .exceptions import CouldNotParseRequirements, RequirementsNotFound
from .handle_setup import from_setup_py
from .poetry_semver import parse_constraint
from .requirement import DetectedRequirement

__all__ = [
    "find_requirements",
    "from_requirements_txt",
    "from_requirements_dir",
    "from_requirements_blob",
    "from_pyproject_toml",
    "from_setup_py",
    "RequirementsNotFound",
    "CouldNotParseRequirements",
]


_PIP_OPTIONS = (
    "-i",
    "--index-url",
    "--extra-index-url",
    "--no-index",
    "-f",
    "--find-links",
    "-r",
)


P = Union[str, Path]


def find_requirements(path: P) -> List[DetectedRequirement]:
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

    if isinstance(path, str):
        path = Path(path)

    setup_py = path / "setup.py"
    if setup_py.exists() and setup_py.is_file():
        try:
            requirements = from_setup_py(setup_py)
            requirements.sort()
            return requirements
        except CouldNotParseRequirements:
            pass

    poetry_toml = path / "pyproject.toml"
    if poetry_toml.exists() and poetry_toml.is_file():
        try:
            requirements = from_pyproject_toml(poetry_toml)
            if len(requirements) > 0:
                requirements.sort()
                return requirements
        except CouldNotParseRequirements:
            pass

    for reqfile_name in ("requirements.txt", "requirements.pip"):
        reqfile = path / reqfile_name
        if reqfile.exists and reqfile.is_file():
            try:
                requirements += from_requirements_txt(reqfile)
            except CouldNotParseRequirements as e:
                pass

    requirements_dir = path / "requirements"
    if requirements_dir.exists() and requirements_dir.is_dir():
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


def from_pyproject_toml(toml_file: P) -> List[DetectedRequirement]:
    requirements = []

    if isinstance(toml_file, str):
        toml_file = Path(toml_file)

    parsed = toml.load(toml_file)
    poetry_section = parsed.get("tool", {}).get("poetry", {})
    dependencies = poetry_section.get("dependencies", {})
    dependencies.update(poetry_section.get("dev-dependencies", {}))

    for name, spec in dependencies.items():
        if name.lower() == "python":
            continue
        if isinstance(spec, dict):
            if "version" in spec:
                spec = spec["version"]
            else:
                req = DetectedRequirement.parse(f"{name}", toml_file)
                if req is not None:
                    requirements.append(req)
                    continue
        parsed_spec = str(parse_constraint(spec))
        if "," not in parsed_spec and "<" not in parsed_spec and ">" not in parsed_spec and "=" not in parsed_spec:
            parsed_spec = f"=={parsed_spec}"

        req = DetectedRequirement.parse(f"{name}{parsed_spec}", toml_file)
        if req is not None:
            requirements.append(req)

    return requirements


def from_requirements_txt(requirements_file: P) -> List[DetectedRequirement]:
    # see http://www.pip-installer.org/en/latest/logic.html
    requirements = []

    if isinstance(requirements_file, str):
        requirements_file = Path(requirements_file)

    with requirements_file.open() as f:
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


def from_requirements_dir(path: P) -> List[DetectedRequirement]:
    requirements = []

    if isinstance(path, str):
        path = Path(path)

    for entry in path.iterdir():
        if not entry.is_file():
            continue
        if entry.name.endswith(".txt") or entry.name.endswith(".pip"):
            requirements += from_requirements_txt(entry)

    return list(set(requirements))


def from_requirements_blob(path: P) -> List[DetectedRequirement]:
    requirements = []

    if isinstance(path, str):
        path = Path(path)

    for entry in path.iterdir():
        if not entry.is_file():
            continue
        m = re.match(r"^(\w*)req(uirement)?s(\w*)\.txt$", entry.name)
        if m is None:
            continue
        if m.group(1).startswith("test") or m.group(3).endswith("test"):
            continue
        requirements += from_requirements_txt(entry)

    return requirements
