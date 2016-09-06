import unittest
from lxml import etree
from bdrxml import foxml, rels

class RelsTest(unittest.TestCase):
    
    def test_multipleRelsInts(self):
      ## datastream
      rids = foxml.Datastream()
      rids.id = u'RELS-INT'
      rids.state = u'A'
      rids.control_group = u'X'
      rids.versionable = u'true'
      ## datastream version
      rids_v = foxml.InlineRelsInt()
      rids_v.id = u'RELS-INT.0'
      rids_v.label = u'Internal Datastream Relationships'
      rids_v.mimetype = u'application/rdf+xml'
      rids_v.format = u'info:fedora/fedora-system:FedoraRELSInt-1.0'
      ## rels-int
      ri = rels.RelsInt()
      ## tiff
      desc = rels.Description()
      desc.about = u'info:fedora/test:123/TIFF'
      desc.download_filename = u'AB_123.tif'
      ## jp2
      desc2 = rels.Description()
      desc2.about = u'info:fedora/test:234/JP2'
      desc2.download_filename = u'AB_123.jp2'
      ## attachments
      ri.descriptions.append( desc )
      ri.descriptions.append( desc2 )
      rids_v.content = ri
      rids.version.append( rids_v )
      ## ouput
      xml =  rids.serialize( pretty=True )
      ## test
      tree = etree.fromstring( xml.decode(u'utf-8', u'replace') )
      descriptions_xpath = u'''/foxml:datastream/foxml:datastreamVersion/foxml:xmlContent/*[namespace-uri()='http://www.w3.org/1999/02/22-rdf-syntax-ns#' and local-name()='RDF']/*[namespace-uri()='http://www.w3.org/1999/02/22-rdf-syntax-ns#' and local-name()='Description']'''
      NS = { u'foxml': u'info:fedora/fedora-system:def/foxml#' }
      description_elements = tree.xpath( descriptions_xpath, namespaces=(NS) )
      filename_element_1 = list( description_elements[0] )[0]
      filename_element_2 = list( description_elements[1] )[0]
      self.assertEqual( len(description_elements), 2 )
      self.assertEqual( type(filename_element_1.text), str )
      self.assertEqual( filename_element_1.text, 'AB_123.tif' )
      self.assertEqual( filename_element_2.text, 'AB_123.jp2' )
    

def suite():
    suite = unittest.makeSuite(RelsTest, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
