import sys
from pathlib import Path
from typing import NoReturn

from . import find_requirements
from .exceptions import RequirementsNotFound
from .formatters import FORMATTERS


def _die(message) -> NoReturn:
    sys.stderr.write("%s\n" % message)
    sys.exit(1)


def run() -> NoReturn:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path.cwd()

    if not path.exists():
        _die("%s does not exist" % path)

    if not path.is_dir():
        _die("%s is not a directory" % path)

    try:
        requirements = find_requirements(path)
    except RequirementsNotFound:
        _die("Unable to find requirements at %s" % path)

    format_name = "requirements_file"  # TODO: other output formats such as JSON
    FORMATTERS[format_name](requirements)
    sys.exit(0)


if __name__ == "__main__":
    run()
