from pathlib import Path

import pytest

from requirements_detector.detect import CouldNotParseRequirements, from_setup_py

_TEST_DIR = Path(__file__).parent / "detection/syntax_error"


def test_setup_py_syntax_error():
    filepath = _TEST_DIR / "setup.py"
    with pytest.raises(CouldNotParseRequirements):
        from_setup_py(filepath)


def test_setup_py_multiline_string():
    filepath = _TEST_DIR / "setup_multiline_string.py"
    from_setup_py(filepath)


def test_regular_indentation():
    filepath = _TEST_DIR / "regular_indentation.py"
    from_setup_py(filepath)
