import re

from astroid import MANAGER, Assign, Const, Keyword, List, Name, Tuple
from astroid.builder import AstroidBuilder

from requirements_detector.__compat__ import AssignName, Call

# PEP263, see http://legacy.python.org/dev/peps/pep-0263/
_ENCODING_REGEXP = re.compile(r"coding[:=]\s*([-\w.]+)")


def _load_file_contents(filepath):
    # This function is a bit of a tedious workaround (AKA 'hack').
    # Astroid calls 'compile' under the hood, which refuses to accept a Unicode
    # object which contains a PEP-263 encoding definition. However if we give
    # Astroid raw bytes, it'll assume ASCII. Therefore we need to detect the encoding
    # here, convert the file contents to a Unicode object, *and also strip the encoding
    # declaration* to avoid the compile step breaking.
    with open(filepath) as f:
        if _PY3K:
            return f.read()

        contents = f.readlines()

        result = []
        encoding_lines = contents[0:2]
        encoding = "utf-8"
        for line in encoding_lines:
            match = _ENCODING_REGEXP.search(line)
            if match is None:
                result.append(line.strip())
            else:
                encoding = match.group(1)

        result += [line.rstrip() for line in contents[2:]]
        result = "\n".join(result)
        return result.decode(encoding)


class SetupWalker(object):
    def __init__(self, ast):
        self._ast = ast
        self._setup_call = None
        self._top_level_assigns = {}
        self.walk()

    def walk(self, node=None):
        top = node is None
        node = node or self._ast

        # test to see if this is a call to setup()
        if isinstance(node, Call):
            for child_node in node.get_children():
                if isinstance(child_node, Name) and child_node.name == "setup":
                    # TODO: what if this isn't actually the distutils setup?
                    self._setup_call = node

        for child_node in node.get_children():
            if top and isinstance(child_node, Assign):
                for target in child_node.targets:
                    if isinstance(target, AssignName):
                        self._top_level_assigns[target.name] = child_node.value
            self.walk(child_node)

    def _get_list_value(self, list_node):
        values = []
        for child_node in list_node.get_children():
            if not isinstance(child_node, Const):
                # we can't handle anything fancy, only constant values
                raise CouldNotParseRequirements
            values.append(child_node.value)
        return values

    def get_requires(self):
        # first, if we have a call to setup, then we can see what its "install_requires" argument is
        if not self._setup_call:
            raise CouldNotParseRequirements

        found_requirements = []

        for child_node in self._setup_call.get_children():
            if not isinstance(child_node, Keyword):
                # do we want to try to handle positional arguments?
                continue

            if child_node.arg not in ("install_requires", "requires"):
                continue

            if isinstance(child_node.value, (List, Tuple)):
                # joy! this is a simple list or tuple of requirements
                # this is a Keyword -> List or Keyword -> Tuple
                found_requirements += self._get_list_value(child_node.value)
                continue

            if isinstance(child_node.value, Name):
                # otherwise, it's referencing a value defined elsewhere
                # this will be a Keyword -> Name
                try:
                    reqs = self._top_level_assigns[child_node.value.name]
                except KeyError:
                    raise CouldNotParseRequirements
                else:
                    if isinstance(reqs, (List, Tuple)):
                        found_requirements += self._get_list_value(reqs)
                        continue

            # otherwise it's something funky and we can't handle it
            raise CouldNotParseRequirements

        # if we've fallen off the bottom with nothing in our list of requirements,
        #  we simply didn't find anything useful
        if len(found_requirements) > 0:
            return found_requirements
        raise CouldNotParseRequirements


def from_setup_py(setup_file):
    try:
        from astroid import AstroidBuildingException
    except ImportError:
        syntax_exceptions = (SyntaxError,)
    else:
        syntax_exceptions = (SyntaxError, AstroidBuildingException)

    try:
        contents = _load_file_contents(setup_file)
        ast = AstroidBuilder(MANAGER).string_build(contents)
    except syntax_exceptions:
        # if the setup file is broken, we can't do much about that...
        raise CouldNotParseRequirements

    walker = SetupWalker(ast)

    requirements = []
    for req in walker.get_requires():
        requirements.append(DetectedRequirement.parse(req, setup_file))

    return [requirement for requirement in requirements if requirement is not None]
