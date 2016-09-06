# coding: utf-8
from __future__ import unicode_literals
import unittest

from eulxml.xmlmap import load_xmlobject_from_string

from bdrxml.foxml import Fox, make
from bdrxml.rels import RelsExt, Cmodel, MemberOf


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
        
    def test_relsIsMemberOf(self):
      r = RelsExt()
      r.about = 'info:fedora/test:124'
      ## add MemberOf to RelsExt
      mo = MemberOf()
      mo.name = 'info:fedora/test:master'
      r.is_member_of.append(mo)
      ## add RelsExt to fox-object
      self.fox.rels_ext = r
      ## test after round-trip
      fox_object = load_xmlobject_from_string( self.fox.serialize(), Fox )
      self.assertTrue( 'info:fedora/test:master' == fox_object.rels_ext.is_member_of[0].name )
      fox_data = fox_object.serialize()
      self.assertTrue( '<rel:isMemberOf rdf:resource="info:fedora/test:master"/>'.encode('utf8') in fox_data )
      

def suite():
    suite = unittest.makeSuite(BasicMakeTest, 'test')
    return suite


if __name__ == '__main__':
    unittest.main()
    
