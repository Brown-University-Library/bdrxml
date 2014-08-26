# encoding=UTF-8
import unittest
from eulxml.xmlmap import load_xmlobject_from_string
from bdrxml import darwincore


SIMPLE_DARWIN_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<SimpleDarwinRecord xmlns="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xmlns:dc="http://purl.org/dc/terms/" xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
  <dc:modified>2009-02-12T12:43:31</dc:modified>
  <dc:language>én</dc:language>
  <dwc:basisOfRecord>Taxon</dwc:basisOfRecord>
  <dwc:scientificName>Ctenomys sociabilis</dwc:scientificName>
  <dwc:acceptedNameUsage>Ctenomys sociabilis Pearson and Christie, 1985</dwc:acceptedNameUsage>
  <dwc:parentNameUsage>Ctenomys Blainville, 1826</dwc:parentNameUsage>
  <dwc:higherClassification>Animalia; Chordata; Vertebrata; Mammalia; Theria; Eutheria; Rodentia; Hystricognatha; Hystricognathi; Ctenomyidae; Ctenomyini; Ctenomys</dwc:higherClassification>
  <dwc:kingdom>Animalia</dwc:kingdom>
  <dwc:phylum>Chordata</dwc:phylum>
  <dwc:class>Mammalia</dwc:class>
  <dwc:order>Rodentia</dwc:order>
  <dwc:family>Ctenomyidae</dwc:family>
  <dwc:genus>Cténomys</dwc:genus>
  <dwc:specificEpithet>sociabilis</dwc:specificEpithet>
  <dwc:taxonRank>species</dwc:taxonRank>
  <dwc:scientificNameAuthorship>Pearson and Christie, 1985</dwc:scientificNameAuthorship>
  <dwc:nomenclaturalCode>ICZN</dwc:nomenclaturalCode>
  <dwc:namePublishedIn>Pearson O. P., and M. I. Christie. 1985. Historia Natural, 5(37):388</dwc:namePublishedIn>
  <dwc:taxonomicStatus>valid</dwc:taxonomicStatus>
  <dwc:dynamicProperties>iucnStatus=vulnerable; distribution=Neuquen, Argentina</dwc:dynamicProperties>
</SimpleDarwinRecord>
'''

class SimpleDarwinRecordTest(unittest.TestCase):

    def setUp(self):
        self.dwc = darwincore.make_simple_darwin_record()

    def test_root(self):
        self.assertEqual(self.dwc.ROOT_NAME, u'SimpleDarwinRecord')


class SimpleDarwinRecordTestLoad(unittest.TestCase):

    def setUp(self):
        self.dwc = load_xmlobject_from_string(SIMPLE_DARWIN_XML, darwincore.SimpleDarwinRecord)

    def test_root(self):
        self.assertEqual(self.dwc.ROOT_NAME, u'SimpleDarwinRecord')
        self.assertEqual(self.dwc.language, u'én')
        self.assertEqual(self.dwc.dwc_scientific_name, u'Ctenomys sociabilis')
        self.assertEqual(self.dwc.dwc_higher_classification, u'Animalia; Chordata; Vertebrata; Mammalia; Theria; Eutheria; Rodentia; Hystricognatha; Hystricognathi; Ctenomyidae; Ctenomyini; Ctenomys')
        self.assertEqual(self.dwc.dwc_kingdom, u'Animalia')
        self.assertEqual(self.dwc.dwc_phylum, u'Chordata')
        self.assertEqual(self.dwc.dwc_class, u'Mammalia')
        self.assertEqual(self.dwc.dwc_order, u'Rodentia')
        self.assertEqual(self.dwc.dwc_family, u'Ctenomyidae')
        self.assertEqual(self.dwc.dwc_genus, u'Cténomys')

    def test_output(self):
        self.assertEqual(self.dwc.serializeDocument(pretty=True), SIMPLE_DARWIN_XML)


class SimpleDarwinRecordSetTest(unittest.TestCase):

    def setUp(self):
        self.dwc = darwincore.make_simple_darwin_record_set()

    def test_root(self):
        self.assertEqual(self.dwc.ROOT_NAME, u'SimpleDarwinRecordSet')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(SimpleDarwinRecordTest('test_root'))
    suite.addTest(SimpleDarwinRecordTestLoad('test_root'))
    suite.addTest(SimpleDarwinRecordTestLoad('test_output'))
    suite.addTest(SimpleDarwinRecordSetTest('test_root'))
    return suite


if __name__ == '__main__':
    unittest.main()
