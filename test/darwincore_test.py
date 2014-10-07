# encoding=UTF-8
import unittest
from eulxml.xmlmap import load_xmlobject_from_string
from bdrxml import darwincore


#test darwin core that's been confirmed to validate (validate again if there are any changes!)
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
    <dwc:nomenclaturalCode>ICZN</dwc:nomenclaturalCode>
    <dwc:namePublishedIn>Pearson O. P., and M. I. Christie. 1985. Historia Natural, 5(37):388</dwc:namePublishedIn>
    <dwc:dynamicProperties>iucnStatus=vulnerable; distribution=Neuquen, Argentina</dwc:dynamicProperties>
 </sdr:SimpleDarwinRecord>
</sdr:SimpleDarwinRecordSet>
'''

#validates
CREATED_SIMPLE_DARWIN_SET_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<sdr:SimpleDarwinRecordSet xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dc="http://purl.org/dc/terms/" xmlns:sdr="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
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
        self.dwc = load_xmlobject_from_string(SIMPLE_DARWIN_SET_XML, darwincore.SimpleDarwinRecordSet)

    def test_root(self):
        self.assertEqual(self.dwc.ROOT_NAME, u'SimpleDarwinRecordSet')
        self.assertEqual(self.dwc.simple_darwin_record.ROOT_NAME, u'SimpleDarwinRecord')
        self.assertEqual(self.dwc.simple_darwin_record.type, u'Test')
        self.assertEqual(self.dwc.simple_darwin_record.language, u'én')
        self.assertEqual(self.dwc.simple_darwin_record.rights, u'Public')
        self.assertEqual(self.dwc.simple_darwin_record.references, u'asdf')
        self.assertEqual(self.dwc.simple_darwin_record.basis_of_record, u'Taxon')
        self.assertEqual(self.dwc.simple_darwin_record.catalog_number, u'catalog number')
        self.assertEqual(self.dwc.simple_darwin_record.recorded_by, u'recorded by')
        self.assertEqual(self.dwc.simple_darwin_record.individual_id, u'individual id')
        self.assertEqual(self.dwc.simple_darwin_record.scientific_name, u'Ctenomys sociabilis')
        self.assertEqual(self.dwc.simple_darwin_record.higher_classification, u'Animalia; Chordata; Vertebrata; Mammalia; Theria; Eutheria; Rodentia; Hystricognatha; Hystricognathi; Ctenomyidae; Ctenomyini; Ctenomys')
        self.assertEqual(self.dwc.simple_darwin_record.kingdom, u'Animalia')
        self.assertEqual(self.dwc.simple_darwin_record.phylum, u'Chordata')
        self.assertEqual(self.dwc.simple_darwin_record.class_, u'Mammalia')
        self.assertEqual(self.dwc.simple_darwin_record.order, u'Rodentia')
        self.assertEqual(self.dwc.simple_darwin_record.genus, u'Cténomys')
        self.assertEqual(self.dwc.simple_darwin_record.accepted_name_usage, u'Ctenomys sociabilis Pearson and Christie, 1985')
        self.assertEqual(self.dwc.simple_darwin_record.specific_epithet, u'sociabilis')
        self.assertEqual(self.dwc.simple_darwin_record.infraspecific_epithet, u'sociabilis sub')
        self.assertEqual(self.dwc.simple_darwin_record.taxon_rank, u'subspecies')
        self.assertEqual(self.dwc.simple_darwin_record.scientific_name_authorship, u'Pearson and Christie, 1985')

    def test_output(self):
        self.assertEqual(self.dwc.serializeDocument(pretty=True), SIMPLE_DARWIN_SET_XML)

    def test_indexing(self):
        index_data = darwincore.SimpleDarwinRecordIndexer(self.dwc.simple_darwin_record).index_data()
        self.assertEqual(index_data['dwc_recorded_by_ssi'], u'recorded by')
        self.assertEqual(index_data['dwc_class_ssi'], u'Mammalia')
        self.assertEqual(index_data['dwc_genus_ssi'], u'Cténomys')
        self.assertEqual(index_data['dwc_identification_id_ssi'], u'én12345')
        self.assertEqual(index_data['dwc_infraspecific_epithet_ssi'], u'sociabilis sub')
        self.assertEqual(index_data['dwc_taxon_rank_ssi'], u'subspecies')
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
