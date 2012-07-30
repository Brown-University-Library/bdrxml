import os
import unittest
from lxml import etree
from eulxml.xmlmap  import load_xmlobject_from_string
import bdrxml
from bdrxml.foxml import Fox, make
from bdrxml.rels import RelsExt

class BasicMakeTest(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.fox = make()
        
    def test_main(self):
        self.fox.pid = 'sample:123'
        fox_string = self.fox.serialize()
        #round trip to make sure we have what we want. 
        read_fox = load_xmlobject_from_string(fox_string, Fox)
        self.assertEqual('sample:123',
                         read_fox.pid)
        #Rels-ext and DC
        #Add
    
    def test_multiple_cmodels(self):
        from bdrxml.rels import RelsExt, Cmodel
        #first model
        r = RelsExt()
        r.about = 'info:fedora/test:123' 
        m1 = Cmodel()
        m1.name = 'info:fedora/bdr-cmodel:commonMetadata'
        r.model.append(m1)
        #second model
        m2 = Cmodel()
        m2.name = 'info:fedora/bdr-cmodel:masterImage'
        r.model.append(m2)
        self.fox.rels_ext = r
        read_fox = load_xmlobject_from_string(self.fox.serialize(), Fox)
        self.assertTrue('info:fedora/bdr-cmodel:commonMetadata' in [m.name for m in read_fox.rels_ext.model])
        self.assertTrue('info:fedora/bdr-cmodel:masterImage' in [m.name for m in read_fox.rels_ext.model])

def suite():
    suite = unittest.makeSuite(BasicMakeTest, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()