import unittest
from test import (
    foxml_test,
    mods_test,
    mets_test,
    rights_test,
    irMetadata_test,
    rels_test,
    darwincore_test
)

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(foxml_test.suite())
    test_suite.addTest(mets_test.suite())
    test_suite.addTest(mods_test.suite())
    test_suite.addTest(rights_test.suite())
    test_suite.addTest(irMetadata_test.suite())
    test_suite.addTest(rels_test.suite())
    test_suite.addTest(darwincore_test.suite())
    return test_suite

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())
