import os
import unittest
from lxml import etree

import eulxml
from eulxml import xmlmap
from eulxml.xmlmap import load_xmlobject_from_string

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
        
    def test_relsIsMemberOf(self):
      import eulxml
      from eulxml import xmlmap
      from bdrxml.rels import RelsExt, MemberOf
      r = RelsExt()
      r.about = 'info:fedora/test:124'
      ## add MemberOf to RelsExt
      mo = MemberOf()
      mo.name = 'info:fedora/test:master'
      r.is_member_of.append(mo)
      ## add RelsExt to fox-object
      self.fox.rels_ext = r
      ## test after round-trip
      fox_object = xmlmap.load_xmlobject_from_string( self.fox.serialize(), Fox )
      self.assertTrue( 'info:fedora/test:master' == fox_object.rels_ext.is_member_of[0].name )
      self.assertTrue( '<rel:isMemberOf rdf:resource="info:fedora/test:master"/>' in fox_object.serialize() )
      
    def test_multipleRelsInt(self):
      ## setup
      from bdrxml.foxml import Datastream, InlineRelsInt, RelsInt
      ds = Datastream()
      ds.id = u'RELS-INT'
      iri = InlineRelsInt()  # container for multiple rels-int
      ## create & add two rels-int nodes
      ri = RelsInt()  # first rels-int
      ri.about = u'aaa'
      ri.download_filename = u'bbb'
      iri.content_list.append( ri )
      ri2 = RelsInt()  # second rels-int
      ri2.about = u'ccc'
      ri2.download_filename = u'ddd'
      iri.content_list.append( ri2 )
      ## parental attachments
      ds.version.append( iri )
      self.fox.datastream.append( ds )
      ## test after round-trip
      fox_obj = xmlmap.load_xmlobject_from_string( self.fox.serialize(), Fox )
      fox_obj_ds = fox_obj.datastream[2]  # not dc or rels-ext
      self.assertTrue( fox_obj_ds.id == u'RELS-INT' )
      NS = { u'foxml': u'info:fedora/fedora-system:def/foxml#' }
      xpath = u'''/foxml:digitalObject/foxml:datastream/foxml:datastreamVersion/foxml:xmlContent/*[namespace-uri()='http://www.w3.org/1999/02/22-rdf-syntax-ns#' and local-name()='RDF']/*[namespace-uri()='http://www.w3.org/1999/02/22-rdf-syntax-ns#' and local-name()='Description']/*[namespace-uri()='info:fedora/fedora-system:def/model#' and local-name()='downloadFilename']'''
      file_name_elements = ds.node.xpath( xpath, namespaces=(NS) )
      self.assertTrue( file_name_elements[0].tag == u'{info:fedora/fedora-system:def/model#}downloadFilename' )
      self.assertTrue( file_name_elements[0].text == u'bbb' )
      self.assertTrue( file_name_elements[1].tag == u'{info:fedora/fedora-system:def/model#}downloadFilename' )
      self.assertTrue( file_name_elements[1].text == u'ddd' )


def suite():
    suite = unittest.makeSuite(BasicMakeTest, 'test')
    return suite


if __name__ == '__main__':
    unittest.main()
    