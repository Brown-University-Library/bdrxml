import sys
import unittest

from test import (
    darwincore_test,
    foxml_test,
    irMetadata_test,
    mets_test,
    mods_test,
    rels_test,
    rights_test,
    xml_regression_test,
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
    test_suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(xml_regression_test))
    return test_suite

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite())
if result.wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)
