# coding: utf-8
from __future__ import unicode_literals
import unittest
from eulxml.xmlmap import load_xmlobject_from_string
from bdrxml import darwincore


SIMPLE_DARWIN_SET_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<sdr:SimpleDarwinRecordSet xmlns:sdr="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xmlns:dc="http://purl.org/dc/terms/" xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
  <sdr:SimpleDarwinRecord>
    <dc:type>Test</dc:type>
    <dc:modified>2009-02-12T12:43:31</dc:modified>
    <dc:language>én</dc:language>
    <dc:license>http://creativecommons.org/licenses/by-sa/3.0/</dc:license>
    <dc:accessRights>not-for-profit use only</dc:accessRights>
    <dc:rightsHolder>Someone</dc:rightsHolder>
    <dc:bibliographicCitation>xyz</dc:bibliographicCitation>
    <dc:references>asdf</dc:references>
    <dwc:typeStatus>holotype of Pinus abies | holotype of Picea abies</dwc:typeStatus>
    <dwc:identificationID>én12345</dwc:identificationID>
    <dwc:catalogNumber>catalog number</dwc:catalogNumber>
    <dwc:basisOfRecord>Taxon</dwc:basisOfRecord>
    <dwc:recordedBy>recorded by</dwc:recordedBy>
    <dwc:recordNumber>2</dwc:recordNumber>
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
    <dwc:taxonID>abcd</dwc:taxonID>
    <dwc:associatedTaxa>host: Quercus alba</dwc:associatedTaxa>
    <dwc:sex>female</dwc:sex>
    <dwc:scientificNameAuthorship>Pearson and Christie, 1985</dwc:scientificNameAuthorship>
    <dwc:municipality>Some City</dwc:municipality>
    <dwc:locality>Locality information</dwc:locality>
    <dwc:locationRemarks>under water since 2005</dwc:locationRemarks>
    <dwc:geodeticDatum>NAD27</dwc:geodeticDatum>
    <dwc:georeferenceVerificationStatus>requires verification</dwc:georeferenceVerificationStatus>
    <dwc:georeferenceSources>GeoLocate</dwc:georeferenceSources>
    <dwc:georeferenceProtocol>Georeferencing Quick Reference Guide</dwc:georeferenceProtocol>
    <dwc:georeferenceRemarks>assumed distance by road (Hwy. 101)</dwc:georeferenceRemarks>
    <dwc:georeferencedBy>Brad Millen (ROM)</dwc:georeferencedBy>
    <dwc:georeferencedDate>1963-03-08</dwc:georeferencedDate>
    <dwc:decimalLatitude>-41.0983423</dwc:decimalLatitude>
    <dwc:decimalLongitude>-121.1761111</dwc:decimalLongitude>
    <dwc:verbatimCoordinates>41 05 54S 121 05 34W</dwc:verbatimCoordinates>
    <dwc:coordinateUncertaintyInMeters>30</dwc:coordinateUncertaintyInMeters>
    <dwc:minimumElevationInMeters>20</dwc:minimumElevationInMeters>
    <dwc:minimumDepthInMeters>15</dwc:minimumDepthInMeters>
    <dwc:nomenclaturalCode>ICZN</dwc:nomenclaturalCode>
    <dwc:namePublishedIn>Pearson O. P., and M. I. Christie. 1985. Historia Natural, 5(37):388</dwc:namePublishedIn>
    <dwc:dynamicProperties>iucnStatus=vulnerable; distribution=Neuquen, Argentina</dwc:dynamicProperties>
    <dwc:collectionID>col 123</dwc:collectionID>
    <dwc:collectionCode>col code</dwc:collectionCode>
    <dwc:year>2002</dwc:year>
    <dwc:month>--05</dwc:month>
    <dwc:day>---02</dwc:day>
    <dwc:startDayOfYear>234</dwc:startDayOfYear>
    <dwc:endDayOfYear>237</dwc:endDayOfYear>
    <dwc:occurrenceID>occ xyz</dwc:occurrenceID>
    <dwc:occurrenceRemarks>found dead on road</dwc:occurrenceRemarks>
    <dwc:institutionCode>BRU</dwc:institutionCode>
    <dwc:dataGeneralizations>Coordinates generalized</dwc:dataGeneralizations>
    <dwc:informationWithheld>collector identities withheld</dwc:informationWithheld>
    <dwc:reproductiveCondition>in bloom</dwc:reproductiveCondition>
    <dwc:lifeStage>egg</dwc:lifeStage>
    <dwc:establishmentMeans>native</dwc:establishmentMeans>
 </sdr:SimpleDarwinRecord>
</sdr:SimpleDarwinRecordSet>
'''

SIMPLE_DARWIN_SNIPPET = '''
  <sdr:SimpleDarwinRecord>
    <dwc:catalogNumber>catalog number</dwc:catalogNumber>
  </sdr:SimpleDarwinRecord>
'''

INVALID_SIMPLE_DARWIN_SET_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<sdr:SimpleDarwinRecordSet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dc="http://purl.org/dc/terms/" xmlns:dwc="http://rs.tdwg.org/dwc/terms/" xmlns:sdr="http://rs.tdwg.org/dwc/xsd/simpledarwincore/" xsi:schemaLocation="http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd">
  <sdr:SimpleDarwinRecord>
    <dwc:random_something>catalog number</dwc:random_something>
  </sdr:SimpleDarwinRecord>
</sdr:SimpleDarwinRecordSet>
'''


class SimpleDarwinRecordTest(unittest.TestCase):

    def test_attribute_name_from_term(self):
        self.assertEqual(darwincore._get_attribute_name_from_term('dc:modified'), 'modified')
        self.assertEqual(darwincore._get_attribute_name_from_term('dc:type'), 'type_')
        self.assertEqual(darwincore._get_attribute_name_from_term('dwc:disposition'), 'disposition')
        self.assertEqual(darwincore._get_attribute_name_from_term('dwc:eventID'), 'event_id')
        self.assertEqual(darwincore._get_attribute_name_from_term('dwc:scientificNameAuthorship'), 'scientific_name_authorship')


class SimpleDarwinRecordSetTestLoad(unittest.TestCase):

    def setUp(self):
        self.dwc = darwincore.make_simple_darwin_record_set()

    def test_1(self):
        self.dwc.create_simple_darwin_record()
        self.dwc.simple_darwin_record.catalog_number = 'catalog number'
        dwc_data = self.dwc.serializeDocument(pretty=True)
        self.assertTrue(SIMPLE_DARWIN_SNIPPET.encode('utf8') in dwc_data)


class SimpleDarwinRecordSetTest(unittest.TestCase):

    def setUp(self):
        self.dwc = load_xmlobject_from_string(SIMPLE_DARWIN_SET_XML.encode('utf8'), darwincore.SimpleDarwinRecordSet)

    def test_validate(self):
        valid = self.dwc.is_valid()
        self.assertTrue(valid)

    def test_invalid(self):
        invalid_dwc = load_xmlobject_from_string(INVALID_SIMPLE_DARWIN_SET_XML.encode('utf8'), darwincore.SimpleDarwinRecordSet)
        valid = invalid_dwc.is_valid()
        self.assertFalse(valid)
        err_str = "<string>:4:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element '{http://rs.tdwg.org/dwc/terms/}random_something': This element is not expected."
        self.assertEqual(str(invalid_dwc.validation_errors()), err_str)

    def test_root(self):
        self.assertEqual(self.dwc.ROOT_NAME, 'SimpleDarwinRecordSet')
        self.assertEqual(self.dwc.simple_darwin_record.ROOT_NAME, 'SimpleDarwinRecord')
        self.assertEqual(self.dwc.simple_darwin_record.type_, 'Test')
        self.assertEqual(self.dwc.simple_darwin_record.language, 'én')
        self.assertEqual(self.dwc.simple_darwin_record.references, 'asdf')
        self.assertEqual(self.dwc.simple_darwin_record.basis_of_record, 'Taxon')
        self.assertEqual(self.dwc.simple_darwin_record.catalog_number, 'catalog number')
        self.assertEqual(self.dwc.simple_darwin_record.recorded_by, 'recorded by')
        self.assertEqual(self.dwc.simple_darwin_record.record_number, '2')
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
        self.assertEqual(self.dwc.simple_darwin_record.taxon_id, 'abcd')
        self.assertEqual(self.dwc.simple_darwin_record.scientific_name_authorship, 'Pearson and Christie, 1985')
        self.assertEqual(self.dwc.simple_darwin_record.municipality, 'Some City')
        self.assertEqual(self.dwc.simple_darwin_record.locality, 'Locality information')
        self.assertEqual(self.dwc.simple_darwin_record.location_remarks, 'under water since 2005')
        self.assertEqual(self.dwc.simple_darwin_record.geodetic_datum, 'NAD27')
        self.assertEqual(self.dwc.simple_darwin_record.decimal_latitude, '-41.0983423')
        self.assertEqual(self.dwc.simple_darwin_record.decimal_longitude, '-121.1761111')
        self.assertEqual(self.dwc.simple_darwin_record.coordinate_uncertainty_in_meters, '30')
        self.assertEqual(self.dwc.simple_darwin_record.verbatim_coordinates, '41 05 54S 121 05 34W')
        self.assertEqual(self.dwc.simple_darwin_record.license, 'http://creativecommons.org/licenses/by-sa/3.0/')
        self.assertEqual(self.dwc.simple_darwin_record.access_rights, 'not-for-profit use only')
        self.assertEqual(self.dwc.simple_darwin_record.type_status, 'holotype of Pinus abies | holotype of Picea abies')
        self.assertEqual(self.dwc.simple_darwin_record.identification_id, 'én12345')
        self.assertEqual(self.dwc.simple_darwin_record.collection_id, 'col 123')
        self.assertEqual(self.dwc.simple_darwin_record.collection_code, 'col code')
        self.assertEqual(self.dwc.simple_darwin_record.year, '2002')
        self.assertEqual(self.dwc.simple_darwin_record.month, '--05')
        self.assertEqual(self.dwc.simple_darwin_record.day, '---02')
        self.assertEqual(self.dwc.simple_darwin_record.occurrence_id, 'occ xyz')
        self.assertEqual(self.dwc.simple_darwin_record.occurrence_remarks, 'found dead on road')
        self.assertEqual(self.dwc.simple_darwin_record.start_day_of_year, '234')
        self.assertEqual(self.dwc.simple_darwin_record.end_day_of_year, '237')
        self.assertEqual(self.dwc.simple_darwin_record.institution_code, 'BRU')
        self.assertEqual(self.dwc.simple_darwin_record.data_generalizations, 'Coordinates generalized')
        self.assertEqual(self.dwc.simple_darwin_record.information_withheld, 'collector identities withheld')
        self.assertEqual(self.dwc.simple_darwin_record.associated_taxa, 'host: Quercus alba')
        self.assertEqual(self.dwc.simple_darwin_record.reproductive_condition, 'in bloom')
        self.assertEqual(self.dwc.simple_darwin_record.life_stage, 'egg')
        self.assertEqual(self.dwc.simple_darwin_record.establishment_means, 'native')
        self.assertEqual(self.dwc.simple_darwin_record.georeferenced_by, 'Brad Millen (ROM)')
        self.assertEqual(self.dwc.simple_darwin_record.georeferenced_date, '1963-03-08')
        self.assertEqual(self.dwc.simple_darwin_record.georeference_sources, 'GeoLocate')
        self.assertEqual(self.dwc.simple_darwin_record.georeference_protocol, 'Georeferencing Quick Reference Guide')
        self.assertEqual(self.dwc.simple_darwin_record.georeference_remarks, 'assumed distance by road (Hwy. 101)')
        self.assertEqual(self.dwc.simple_darwin_record.georeference_verification_status, 'requires verification')
        self.assertEqual(self.dwc.simple_darwin_record.minimum_elevation_in_meters, '20')
        self.assertEqual(self.dwc.simple_darwin_record.minimum_depth_in_meters, '15')
        self.assertEqual(self.dwc.simple_darwin_record.sex, 'female')

    def test_output(self):
        self.assertEqual(self.dwc.serializeDocument(pretty=True), SIMPLE_DARWIN_SET_XML.encode('utf8'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(SimpleDarwinRecordTest('test_attribute_name_from_term'))
    suite.addTest(SimpleDarwinRecordSetTest('test_root'))
    suite.addTest(SimpleDarwinRecordSetTest('test_output'))
    suite.addTest(SimpleDarwinRecordSetTest('test_validate'))
    suite.addTest(SimpleDarwinRecordSetTest('test_invalid'))
    suite.addTest(SimpleDarwinRecordSetTestLoad('test_1'))
    return suite


if __name__ == '__main__':
    unittest.main()
