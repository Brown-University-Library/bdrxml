# coding: utf-8
from __future__ import unicode_literals
import unittest
from eulxml.xmlmap import load_xmlobject_from_string
from bdrxml import darwincore


#this dwc should validate, except for dc:rights and dwc:individualID fields
SIMPLE_DARWIN_SET_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<sdr:SimpleDarwinRecordSet xmlns:sdr="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xmlns:dc="http://purl.org/dc/terms/" xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
  <sdr:SimpleDarwinRecord>
    <dc:type>Test</dc:type>
    <dc:modified>2009-02-12T12:43:31</dc:modified>
    <dc:language>én</dc:language>
    <dc:rights>Public</dc:rights>
    <dc:rightsHolder>Someone</dc:rightsHolder>
    <dc:bibliographicCitation>xyz</dc:bibliographicCitation>
    <dc:references>asdf</dc:references>
    <dwc:identificationID>én12345</dwc:identificationID>
    <dwc:catalogNumber>catalog number</dwc:catalogNumber>
    <dwc:basisOfRecord>Taxon</dwc:basisOfRecord>
    <dwc:recordedBy>recorded by</dwc:recordedBy>
    <dwc:recordNumber>2</dwc:recordNumber>
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
    <dwc:infraspecificEpithet>sociabilis sub</dwc:infraspecificEpithet>
    <dwc:taxonRank>subspecies</dwc:taxonRank>
    <dwc:scientificNameAuthorship>Pearson and Christie, 1985</dwc:scientificNameAuthorship>
    <dwc:municipality>Some City</dwc:municipality>
    <dwc:locality>Locality information</dwc:locality>
    <dwc:nomenclaturalCode>ICZN</dwc:nomenclaturalCode>
    <dwc:namePublishedIn>Pearson O. P., and M. I. Christie. 1985. Historia Natural, 5(37):388</dwc:namePublishedIn>
    <dwc:dynamicProperties>iucnStatus=vulnerable; distribution=Neuquen, Argentina</dwc:dynamicProperties>
 </sdr:SimpleDarwinRecord>
</sdr:SimpleDarwinRecordSet>
'''

#validates
CREATED_SIMPLE_DARWIN_SET_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<sdr:SimpleDarwinRecordSet xmlns:dc="http://purl.org/dc/terms/" xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:sdr="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
  <sdr:SimpleDarwinRecord>
    <dwc:catalogNumber>catalog number</dwc:catalogNumber>
  </sdr:SimpleDarwinRecord>
</sdr:SimpleDarwinRecordSet>
'''


class SimpleDarwinRecordSetTestLoad(unittest.TestCase):

    def setUp(self):
        self.dwc = darwincore.make_simple_darwin_record_set()

    def test_1(self):
        self.dwc.create_simple_darwin_record()
        self.dwc.simple_darwin_record.catalog_number = 'catalog number'
        self.assertEqual(self.dwc.serializeDocument(pretty=True), CREATED_SIMPLE_DARWIN_SET_XML)


class SimpleDarwinRecordSetTest(unittest.TestCase):

    def setUp(self):
        self.dwc = load_xmlobject_from_string(SIMPLE_DARWIN_SET_XML.encode('utf8'), darwincore.SimpleDarwinRecordSet)

    def test_root(self):
        self.assertEqual(self.dwc.ROOT_NAME, 'SimpleDarwinRecordSet')
        self.assertEqual(self.dwc.simple_darwin_record.ROOT_NAME, 'SimpleDarwinRecord')
        self.assertEqual(self.dwc.simple_darwin_record.type, 'Test')
        self.assertEqual(self.dwc.simple_darwin_record.language, 'én')
        self.assertEqual(self.dwc.simple_darwin_record.rights, 'Public')
        self.assertEqual(self.dwc.simple_darwin_record.references, 'asdf')
        self.assertEqual(self.dwc.simple_darwin_record.basis_of_record, 'Taxon')
        self.assertEqual(self.dwc.simple_darwin_record.catalog_number, 'catalog number')
        self.assertEqual(self.dwc.simple_darwin_record.recorded_by, 'recorded by')
        self.assertEqual(self.dwc.simple_darwin_record.record_number, '2')
        self.assertEqual(self.dwc.simple_darwin_record.individual_id, 'individual id')
        self.assertEqual(self.dwc.simple_darwin_record.scientific_name, 'Ctenomys sociabilis')
        self.assertEqual(self.dwc.simple_darwin_record.higher_classification, 'Animalia; Chordata; Vertebrata; Mammalia; Theria; Eutheria; Rodentia; Hystricognatha; Hystricognathi; Ctenomyidae; Ctenomyini; Ctenomys')
        self.assertEqual(self.dwc.simple_darwin_record.kingdom, 'Animalia')
        self.assertEqual(self.dwc.simple_darwin_record.phylum, 'Chordata')
        self.assertEqual(self.dwc.simple_darwin_record.class_, 'Mammalia')
        self.assertEqual(self.dwc.simple_darwin_record.order, 'Rodentia')
        self.assertEqual(self.dwc.simple_darwin_record.genus, 'Cténomys')
        self.assertEqual(self.dwc.simple_darwin_record.accepted_name_usage, 'Ctenomys sociabilis Pearson and Christie, 1985')
        self.assertEqual(self.dwc.simple_darwin_record.specific_epithet, 'sociabilis')
        self.assertEqual(self.dwc.simple_darwin_record.infraspecific_epithet, 'sociabilis sub')
        self.assertEqual(self.dwc.simple_darwin_record.taxon_rank, 'subspecies')
        self.assertEqual(self.dwc.simple_darwin_record.scientific_name_authorship, 'Pearson and Christie, 1985')
        self.assertEqual(self.dwc.simple_darwin_record.municipality, 'Some City')
        self.assertEqual(self.dwc.simple_darwin_record.locality, 'Locality information')

    def test_output(self):
        self.assertEqual(self.dwc.serializeDocument(pretty=True), SIMPLE_DARWIN_SET_XML.encode('utf8'))

class SimpleDarwinRecordSetIndexerTest(unittest.TestCase):

    def setUp(self):
        self.dwc = load_xmlobject_from_string(SIMPLE_DARWIN_SET_XML.encode('utf8'), darwincore.SimpleDarwinRecordSet)

    def test_indexing(self):
        index_data = darwincore.SimpleDarwinRecordIndexer(self.dwc.simple_darwin_record).index_data()
        self.assertEqual(index_data['dwc_recorded_by_ssi'], 'recorded by')
        self.assertEqual(index_data['dwc_record_number_ssi'], '2')
        self.assertEqual(index_data['dwc_class_ssi'], 'Mammalia')
        self.assertEqual(index_data['dwc_genus_ssi'], 'Cténomys')
        self.assertEqual(index_data['dwc_identification_id_ssi'], 'én12345')
        self.assertEqual(index_data['dwc_infraspecific_epithet_ssi'], 'sociabilis sub')
        self.assertEqual(index_data['dwc_taxon_rank_ssi'], 'subspecies')
        self.assertEqual(index_data['dwc_taxon_rank_abbr_ssi'], 'subsp.')
        self.assertTrue('dwc_family_ssi' not in index_data)

    def test_sparse_record(self):
        dwc = load_xmlobject_from_string(CREATED_SIMPLE_DARWIN_SET_XML.encode('utf8'), darwincore.SimpleDarwinRecordSet)
        index_data = darwincore.SimpleDarwinRecordIndexer(dwc.simple_darwin_record).index_data()
        self.assertEqual(index_data, {'dwc_catalog_number_ssi': 'catalog number'})

    def test_taxon_rank_abbr(self):
        dwc = darwincore.make_simple_darwin_record_set()
        dwc.create_simple_darwin_record()
        indexer = darwincore.SimpleDarwinRecordIndexer(dwc.simple_darwin_record)
        self.assertEqual(indexer._get_taxon_rank_abbr(), '')
        dwc.simple_darwin_record.taxon_rank = 'variety'
        self.assertEqual(indexer._get_taxon_rank_abbr(), 'var.')
        dwc.simple_darwin_record.taxon_rank = 'subspecies'
        self.assertEqual(indexer._get_taxon_rank_abbr(), 'subsp.')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(SimpleDarwinRecordSetTest('test_root'))
    suite.addTest(SimpleDarwinRecordSetTest('test_output'))
    suite.addTest(SimpleDarwinRecordSetIndexerTest('test_indexing'))
    suite.addTest(SimpleDarwinRecordSetIndexerTest('test_sparse_record'))
    suite.addTest(SimpleDarwinRecordSetIndexerTest('test_taxon_rank_abbr'))
    suite.addTest(SimpleDarwinRecordSetTestLoad('test_1'))
    return suite


if __name__ == '__main__':
    unittest.main()
