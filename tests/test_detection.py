from pathlib import Path
from unittest import TestCase

from requirements_detector.detect import (
    CouldNotParseRequirements,
    from_pyproject_toml,
    from_requirements_blob,
    from_requirements_dir,
    from_requirements_txt,
    from_setup_py,
)
from requirements_detector.requirement import DetectedRequirement

_TEST_DIR = Path(__file__).parent / "detection"


class DependencyDetectionTest(TestCase):
    def _expected(self, *requirements):
        return sorted(DetectedRequirement.parse(req) for req in requirements)

    def test_requirements_txt_parsing(self):
        filepath = _TEST_DIR / "test1/requirements.txt"
        dependencies = from_requirements_txt(filepath)

        expected = self._expected(
            "amqp!=1.0.13",
            "Django>=1.5.0",
            "six<1.4,>=1.3.0",
            "South==0.8.2",
        )

        self.assertEqual(expected, sorted(dependencies))

    def test_requirements_dir_parsing(self):
        filepath = _TEST_DIR / "test2/requirements"
        dependencies = from_requirements_dir(filepath)

        expected = self._expected(
            "amqp==1.0.13",
            "anyjson==0.3.3",
            "Django==1.5.2",
            "South==0.8.2",
        )

        self.assertEqual(expected, sorted(dependencies))

    def test_requirements_blob_parsing(self):
        filepath = _TEST_DIR / "test3"
        dependencies = from_requirements_blob(filepath)

        expected = self._expected(
            "amqp==1.0.13",
            "anyjson==0.3.3",
            "django-gubbins==1.1.2",
        )

        self.assertEqual(expected, sorted(dependencies))

    def test_invalid_requirements_txt(self):
        filepath = _TEST_DIR / "test5/invalid_requirements.txt"
        dependencies = from_requirements_txt(filepath)
        expected = self._expected("django<1.6", "django")
        self.assertEqual(expected, sorted(dependencies))

    def test_requirements_txt(self):
        filepath = _TEST_DIR / "test6/requirements.txt"
        reqs = from_requirements_txt(filepath)
        self.assertTrue(len(reqs) > 0)

    def test_poetry_requirements_txt(self):
        # tests parsing a requirements format generated by 'poetry export'
        filepath = _TEST_DIR / "test7/poetry-format-requirements.txt"
        reqs = from_requirements_txt(str(filepath))
        self.assertTrue(len(reqs) > 0)

    def test_pyproject_toml(self):
        # tests parsing a pyproject.toml file
        filepath = _TEST_DIR / "test8/pyproject.toml"
        reqs = from_pyproject_toml(str(filepath))
        self.assertTrue(len(reqs) > 0)

        names = [req.name for req in reqs]
        self.assertIn("click", names)
        self.assertIn("twine", names)
        self.assertIn("requests", names)
        self.assertIn("pytest", names)

        pyroma = [req for req in reqs if req.name == "pyroma"][0]
        self.assertEqual(2, len(pyroma.version_specs[0]))
        self.assertEqual("pyroma>=2.4", str(pyroma))

    def _test_setup_py(self, setup_py_file, *expected):
        filepath = _TEST_DIR / "test4" / setup_py_file
        dependencies = from_setup_py(str(filepath))
        expected = self._expected(*expected)
        self.assertEqual(expected, sorted(dependencies))

    def _test_setup_py_not_parseable(self, setup_py_file):
        filepath = _TEST_DIR / "test4" / setup_py_file
        self.assertRaises(CouldNotParseRequirements, from_setup_py, filepath)

    def test_simple_setup_py_parsing(self):
        self._test_setup_py("simple.py", "Django==1.5.0", "django-gubbins==1.1.2")

    def test_setup_py_reqs_defined_in_file_parsing(self):
        self._test_setup_py("in_file.py", "Django==1.5.0", "django-gubbins==1.1.2")

    def test_setup_py_tuple(self):
        self._test_setup_py("tuple.py", "Django==1.5.0", "django-gubbins==1.1.2")

    def test_subscript_assign(self):
        self._test_setup_py(
            "subscript_assign.py", "Django==1.5.0", "django-gubbins==1.1.2"
        )

    def test_utf8_setup_py(self):
        self._test_setup_py("utf8.py", "Django==1.5.0", "django-gubbins==1.1.2")

    def test_requires_setup_py(self):
        self._test_setup_py(
            "uses_requires.py", "Django==1.5.0", "django-gubbins==1.1.2"
        )

    def test_requires_and_install_requires_setup_py(self):
        self._test_setup_py(
            "uses_requires_and_install_requires.py",
            "Django==1.5.0",
            "django-gubbins==1.1.2",
        )

    def test_callable_install_requires(self):
        self._test_setup_py_not_parseable("callable.py")
