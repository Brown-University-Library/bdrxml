import unittest
from test import foxml, mods, mets

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(foxml.suite())
    test_suite.addTest(mets.suite())
    test_suite.addTest(mods.suite())
    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())