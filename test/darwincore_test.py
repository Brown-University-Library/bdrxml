# encoding=UTF-8
import unittest
from eulxml.xmlmap import load_xmlobject_from_string
from bdrxml import darwincore


DARWINCORE_INNER_CONTENT = '''  <dc:modified>2009-02-12T12:43:31</dc:modified>
  <dc:identifier>én</dc:identifier>
  <dwc:catalogNumber>catalog number</dwc:catalogNumber>
  <dwc:basisOfRecord>Taxon</dwc:basisOfRecord>
  <dwc:recordedBy>recorded by</dwc:recordedBy>
  <dwc:individualID>individual id</dwc:individualID>
  <dwc:scientificName>Ctenomys sociabilis</dwc:scientificName>
  <dwc:acceptedNameUsage>Ctenomys sociabilis Pearson and Christie, 1985</dwc:acceptedNameUsage>
  <dwc:parentNameUsage>Ctenomys Blainville, 1826</dwc:parentNameUsage>
  <dwc:higherClassification>Animalia; Chordata; Vertebrata; Mammalia; Theria; Eutheria; Rodentia; Hystricognatha; Hystricognathi; Ctenomyidae; Ctenomyini; Ctenomys</dwc:higherClassification>
  <dwc:kingdom>Animalia</dwc:kingdom>
  <dwc:phylum>Chordata</dwc:phylum>
  <dwc:class>Mammalia</dwc:class>
  <dwc:order>Rodentia</dwc:order>
  <dwc:genus>Cténomys</dwc:genus>
  <dwc:specificEpithet>sociabilis</dwc:specificEpithet>
  <dwc:taxonRank>species</dwc:taxonRank>
  <dwc:scientificNameAuthorship>Pearson and Christie, 1985</dwc:scientificNameAuthorship>
  <dwc:nomenclaturalCode>ICZN</dwc:nomenclaturalCode>
  <dwc:namePublishedIn>Pearson O. P., and M. I. Christie. 1985. Historia Natural, 5(37):388</dwc:namePublishedIn>
  <dwc:dynamicProperties>iucnStatus=vulnerable; distribution=Neuquen, Argentina</dwc:dynamicProperties>'''

SIMPLE_DARWIN_SET_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<SimpleDarwinRecordSet xmlns="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xmlns:sdr="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xmlns:dc="http://purl.org/dc/terms/" xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
  <sdr:SimpleDarwinRecord>
%s
  </sdr:SimpleDarwinRecord>
</SimpleDarwinRecordSet>
''' % DARWINCORE_INNER_CONTENT

CREATED_SIMPLE_DARWIN_SET_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<SimpleDarwinRecordSet xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dc="http://purl.org/dc/terms/" xmlns:sdr="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xsi:schemaLocation="http://rs.tdwg.org/dwc/dwcrecord/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
  <sdr:SimpleDarwinRecord>
    <dwc:catalogNumber>catalog number</dwc:catalogNumber>
  </sdr:SimpleDarwinRecord>
</SimpleDarwinRecordSet>
'''


class SimpleDarwinRecordSetTestLoad(unittest.TestCase):

    def setUp(self):
        self.dwc = darwincore.make_simple_darwin_record_set()

    def test_1(self):
        self.dwc.create_simple_darwin_record()
        self.dwc.simple_darwin_record.dwc_catalog_number = 'catalog number'
        self.assertEqual(self.dwc.serializeDocument(pretty=True), CREATED_SIMPLE_DARWIN_SET_XML)


class SimpleDarwinRecordSetTest(unittest.TestCase):

    def setUp(self):
        self.dwc = load_xmlobject_from_string(SIMPLE_DARWIN_SET_XML, darwincore.SimpleDarwinRecordSet)

    def test_root(self):
        self.assertEqual(self.dwc.ROOT_NAME, u'SimpleDarwinRecordSet')
        self.assertEqual(self.dwc.simple_darwin_record.ROOT_NAME, u'SimpleDarwinRecord')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_basis_of_record, u'Taxon')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_catalog_number, u'catalog number')
        self.assertEqual(self.dwc.simple_darwin_record.identifier, u'én')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_recorded_by, u'recorded by')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_individual_id, u'individual id')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_scientific_name, u'Ctenomys sociabilis')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_higher_classification, u'Animalia; Chordata; Vertebrata; Mammalia; Theria; Eutheria; Rodentia; Hystricognatha; Hystricognathi; Ctenomyidae; Ctenomyini; Ctenomys')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_kingdom, u'Animalia')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_phylum, u'Chordata')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_class, u'Mammalia')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_order, u'Rodentia')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_genus, u'Cténomys')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_accepted_name_usage, u'Ctenomys sociabilis Pearson and Christie, 1985')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_specific_epithet, u'sociabilis')
        self.assertEqual(self.dwc.simple_darwin_record.dwc_scientific_name_authorship, u'Pearson and Christie, 1985')

    def test_output(self):
        self.assertEqual(self.dwc.serializeDocument(pretty=True), SIMPLE_DARWIN_SET_XML)

    def test_indexing(self):
        index_data = darwincore.SimpleDarwinRecordIndexer(self.dwc.simple_darwin_record).index_data()
        self.assertEqual(index_data['dwc_recorded_by_ssi'], u'recorded by')
        self.assertEqual(index_data['dwc_genus_ssi'], u'Cténomys')
        self.assertEqual(index_data['dwc_identifier_ssi'], u'én')
        self.assertTrue('dwc_family_ssi' not in index_data)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(SimpleDarwinRecordSetTest('test_root'))
    suite.addTest(SimpleDarwinRecordSetTest('test_output'))
    suite.addTest(SimpleDarwinRecordSetTest('test_indexing'))
    suite.addTest(SimpleDarwinRecordSetTestLoad('test_1'))
    return suite


if __name__ == '__main__':
    unittest.main()
