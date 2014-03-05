import os
from unittest import TestCase
from requirements_detector.detect import from_setup_py, CouldNotParseRequirements


class SyntaxErrorTest(TestCase):

    def test_setup_py_syntax_error(self):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/syntax_error/setup.py')
        self.assertRaises(CouldNotParseRequirements, from_setup_py, filepath)
