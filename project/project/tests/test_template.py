# project/testTemplate.py

from django.test import TestCase
from project.views.design import stringy


class StringyTestCase(TestCase):
    def testStringy(self):
        string = stringy("strings")
        self.assertEqual(string, "strings")
