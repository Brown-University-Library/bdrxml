import unittest
from test import foxml, mods, mets, rights, irMetadata, rels_test

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(foxml.suite())
    test_suite.addTest(mets.suite())
    test_suite.addTest(mods.suite())
    test_suite.addTest(rights.suite())
    test_suite.addTest(irMetadata.suite())
    test_suite.addTest(rels_test.suite())
    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
