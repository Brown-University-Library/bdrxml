import os
import unittest
from lxml import etree
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.mods import Mods, make_mods, MODS_SCHEMA

class ModsReadWrite(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.mods = make_mods()
        
    def test_round_trip(self):
        self.mods.title = "Sample title"
        self.mods.publisher = "BUL"
        mods_str = self.mods.serialize(pretty=False)
        loaded = load_xmlobject_from_string(mods_str, Mods)
        self.assertEqual(loaded.title, 'Sample title')
        self.assertEqual(loaded.publisher, 'BUL')
        self.assertTrue(MODS_SCHEMA in loaded.schema_location)
        


def suite():
    suite = unittest.makeSuite(ModsReadWrite, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()