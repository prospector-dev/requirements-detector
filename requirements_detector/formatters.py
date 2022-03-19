import sys
from typing import List

from .requirement import DetectedRequirement


def requirements_file(requirements_list: List[DetectedRequirement]) -> None:
    for requirement in requirements_list:
        sys.stdout.write(requirement.pip_format())
        sys.stdout.write("\n")


FORMATTERS = {"requirements_file": requirements_file}
