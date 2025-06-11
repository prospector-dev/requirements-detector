from unittest import TestCase
from urllib import parse as urlparse

from requirements_detector.requirement import (
    DetectedRequirement,
    _parse_egg_name,
    _strip_fragment,
)


class TestRequirementParsing(TestCase):
    def _test(self, requirement, name=None, version_specs=None, url=None):
        req = DetectedRequirement.parse(requirement)
        self.assertEqual(name, req.name)
        if version_specs is None:
            self.assertEqual([], req.version_specs)
        else:
            for spec in version_specs:
                self.assertTrue(spec in req.version_specs)
        self.assertEqual(url, req.url)

    def test_basic_requirement(self):
        self._test("Django", "Django")
        self._test("celery", "celery")

    def test_requirement_with_versions(self):
        self._test("Django==1.5.2", "Django", [("==", "1.5.2")])
        self._test("South>0.8", "South", [(">", "0.8")])
        self._test(
            "django-gubbins!=1.1.1,>1.1",
            "django-gubbins",
            [("!=", "1.1.1"), (">", "1.1")],
        )

    def test_relative_file_path(self):
        self._test("../somelib", url="../somelib")

    def test_vcs_url(self):
        self._test(
            "git+ssh://git@github.com/something/somelib.git",
            url="git+ssh://git@github.com/something/somelib.git",
        )
        self._test(
            "git+ssh://git@github.com/something/somelib.git#egg=somelib",
            name="somelib",
            url="git+ssh://git@github.com/something/somelib.git",
        )
        self._test(
            "git://github.com/peeb/django-mollie-ideal.git#egg=mollie",
            name="mollie",
            url="git+git://github.com/peeb/django-mollie-ideal.git",
        )

    def test_archive_url(self):
        self._test(
            "http://example.com/somelib.tar.gz", url="http://example.com/somelib.tar.gz"
        )
        self._test(
            "http://example.com/somelib.tar.gz#egg=somelib",
            name="somelib",
            url="http://example.com/somelib.tar.gz",
        )

    def test_editable_relative_path(self):
        self._test("-e ../somelib", url="../somelib")

    def test_editable_vcs_url(self):
        self._test(
            "--editable git+ssh://git@github.com/something/somelib.git#egg=somelib",
            name="somelib",
            url="git+ssh://git@github.com/something/somelib.git",
        )

    def test_comments(self):
        self._test("celery == 0.1 # comment", "celery", [("==", "0.1")])
        self._test("celery == 0.1\t# comment", "celery", [("==", "0.1")])
        self._test(
            "somelib == 0.15 # pinned to 0.15 (https://github.com/owner/repo/issues/111)",
            "somelib",
            [("==", "0.15")],
        )
        self._test(
            "http://example.com/somelib.tar.gz # comment",
            url="http://example.com/somelib.tar.gz",
        )
        self._test(
            "http://example.com/somelib.tar.gz#egg=somelib # url comment http://foo.com/bar",
            name="somelib",
            url="http://example.com/somelib.tar.gz",
        )


class TestEggFragmentParsing(TestCase):
    def test_simple(self):
        self.assertEqual("somelib", _parse_egg_name("egg=somelib"))

    def test_no_egg_value(self):
        self.assertTrue(_parse_egg_name("a=b&c=2") is None)

    def test_no_pairs(self):
        self.assertTrue(_parse_egg_name("somelib") is None)

    def test_first_egg_val(self):
        self.assertEqual("somelib", _parse_egg_name("egg=somelib&egg=anotherlib"))

    def test_multiple_fragment_values(self):
        self.assertEqual("somelib", _parse_egg_name("a=1&egg=somelib&b=2"))


class TestFragmentStripping(TestCase):
    def test_stripping(self):
        url = "http://example.com/index.html?a=b&c=2#some_fragment"
        parts = urlparse.urlparse(url)
        self.assertEqual(
            "http://example.com/index.html?a=b&c=2", _strip_fragment(parts)
        )
