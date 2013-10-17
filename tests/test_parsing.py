
from unittest import TestCase
from requirements_detector.requirement import DetectedRequirement


class TestRequirementParsing(TestCase):

    def test_basic_requirement(self):
        req = DetectedRequirement.parse('Django')
        print req
