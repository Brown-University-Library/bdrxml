import os
import unittest
from lxml import etree
from eulxml.xmlmap  import load_xmlobject_from_string, load_xmlobject_from_file
from bdrxml.mets import BDRMets, make_mets
from bdrxml.mods import Mods, MODS_SCHEMA
from eulxml import xmlmap

BASE = os.path.dirname(os.path.abspath(__file__))

class MetsReadWrite(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.mets = load_xmlobject_from_file(os.path.join(BASE, 'data/cdi_mets.xml'),
                                             BDRMets)
        
    def test_read(self):
        #print self.mets.serialize(pretty=True)
        self.assertEqual(self.mets.rights.holder.name, "Brown University")
        self.assertEqual(self.mets.mods.title, "Camp Grant Massacre")
        
    def test_create(self):
        import bdrxml
        from bdrxml.foxml import make
        from bdrxml import mods
        from bdrxml.foxml import Datastream, DatastreamVersion, InlineMets
        mets = make_mets()
        #mods
        mods_section = mods.make_mods()
        mods_section.title = 'sample'
        mets.create_mdwrap()
        mets.mdwrap.id = 'MODS'
        mets.mods = mods_section
        #ir
        mets.create_ir()
        mets.ir.filename = 'sample.txt'
        #structMap
        mets.create_structmap()  # not used but required for valid mets
        #serialize
        created_string = mets.serialize()
        #load
        loaded = load_xmlobject_from_string(created_string, BDRMets)
        #test
        self.assertEqual(loaded.mods.title, 'sample')
        self.assertEqual(loaded.ir.filename, 'sample.txt')
        self.assertEqual( type(loaded.structmap), bdrxml.mets.StructMap )
        
        #TO DO - finish.  Also test helper called by studio.


def suite():
    suite = unittest.makeSuite(MetsReadWrite, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
