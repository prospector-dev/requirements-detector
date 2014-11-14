import os
from unittest import TestCase
from requirements_detector.detect import from_requirements_txt, from_requirements_dir, \
    from_requirements_blob, from_setup_py, CouldNotParseRequirements
from requirements_detector.requirement import DetectedRequirement


class DependencyDetectionTest(TestCase):

    def _expected(self, *requirements):
        return [DetectedRequirement.parse(req) for req in requirements]

    def test_requirements_txt_parsing(self):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/test1/requirements.txt')
        dependencies = from_requirements_txt(filepath)

        expected = self._expected(
            'amqp!=1.0.13',
            'Django>=1.5.0',
            'six<1.4,>=1.3.0',
            'South==0.8.2',
        )

        self.assertEqual(expected, sorted(dependencies))

    def test_requirements_dir_parsing(self):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/test2/requirements')
        dependencies = from_requirements_dir(filepath)

        expected = self._expected(
            'amqp==1.0.13',
            'anyjson==0.3.3',
            'Django==1.5.2',
            'South==0.8.2',
        )

        self.assertEqual(expected, sorted(dependencies))

    def test_requirements_blob_parsing(self):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/test3')
        dependencies = from_requirements_blob(filepath)

        expected = self._expected(
            'amqp==1.0.13',
            'anyjson==0.3.3',
            'django-gubbins==1.1.2',
        )

        self.assertEqual(expected, sorted(dependencies))

    def test_invalid_requirements_txt(self):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/test5/invalid_requirements.txt')
        dependencies = from_requirements_txt(filepath)
        expected = self._expected('django<1.6', 'django')
        self.assertEqual(expected, sorted(dependencies))

    def test_invalid_requirements_txt(self):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/test6/requirements.txt')
        from_requirements_txt(filepath)

    def _test_setup_py(self, setup_py_file, *expected):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/test4', setup_py_file)
        dependencies = from_setup_py(filepath)
        expected = self._expected(*expected)
        self.assertEqual(expected, sorted(dependencies))

    def _test_setup_py_not_parseable(self, setup_py_file):
        filepath = os.path.join(os.path.dirname(__file__), 'detection/test4', setup_py_file)
        self.assertRaises(CouldNotParseRequirements, from_setup_py, filepath)

    def test_simple_setup_py_parsing(self):
        self._test_setup_py('simple.py', 'Django==1.5.0', 'django-gubbins==1.1.2')

    def test_setup_py_reqs_defined_in_file_parsing(self):
        self._test_setup_py('in_file.py', 'Django==1.5.0', 'django-gubbins==1.1.2')

    def test_setup_py_tuple(self):
        self._test_setup_py('tuple.py', 'Django==1.5.0', 'django-gubbins==1.1.2')

    def test_subscript_assign(self):
        self._test_setup_py('subscript_assign.py', 'Django==1.5.0', 'django-gubbins==1.1.2')

    def test_utf8_setup_py(self):
        self._test_setup_py('utf8.py', 'Django==1.5.0', 'django-gubbins==1.1.2')

    def test_callable_install_requires(self):
        self._test_setup_py_not_parseable('callable.py')