# coding: utf-8
from __future__ import unicode_literals
from eulxml import xmlmap
from eulxml.xmlmap import dc


XMLNS = 'http://rs.tdwg.org/dwc/xsd/simpledarwincore/'
DCNS = 'http://purl.org/dc/terms/'
DWCNS = 'http://rs.tdwg.org/dwc/terms/'
XSINS = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_SCHEMA_LOCATION = 'http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd'


class SimpleDarwinRecord(xmlmap.XmlObject):
    ROOT_NAME = 'SimpleDarwinRecord'
    XSD_SCHEMA = None
    ROOT_NAMESPACES = {}

    type_ = xmlmap.StringField('dc:type')
    modified = xmlmap.StringField('dc:modified')
    language = xmlmap.StringField('dc:language')
    rights = xmlmap.StringField('dc:rights') #deprecated - probably use license instead
    access_rights = xmlmap.StringField('dc:accessRights')
    license = xmlmap.StringField('dc:license')
    rights_holder = xmlmap.StringField('dc:rightsHolder')
    bibliographic_citation = xmlmap.StringField('dc:bibliographicCitation')
    references = xmlmap.StringField('dc:references')
    type_status = xmlmap.StringField('dwc:typeStatus')
    basis_of_record = xmlmap.StringField('dwc:basisOfRecord')
    catalog_number = xmlmap.StringField('dwc:catalogNumber')
    recorded_by = xmlmap.StringField('dwc:recordedBy')
    record_number = xmlmap.StringField('dwc:recordNumber')
    event_date = xmlmap.StringField('dwc:eventDate')
    verbatim_event_date = xmlmap.StringField('dwc:verbatimEventDate')
    scientific_name = xmlmap.StringField('dwc:scientificName')
    higher_classification = xmlmap.StringField('dwc:higherClassification')
    kingdom = xmlmap.StringField('dwc:kingdom')
    phylum = xmlmap.StringField('dwc:phylum')
    class_ = xmlmap.StringField('dwc:class') #class_ because of class keyword
    order = xmlmap.StringField('dwc:order')
    family = xmlmap.StringField('dwc:family')
    genus = xmlmap.StringField('dwc:genus')
    specific_epithet = xmlmap.StringField('dwc:specificEpithet')
    infraspecific_epithet = xmlmap.StringField('dwc:infraspecificEpithet')
    taxon_rank = xmlmap.StringField('dwc:taxonRank')
    accepted_name_usage = xmlmap.StringField('dwc:acceptedNameUsage')
    scientific_name_authorship = xmlmap.StringField('dwc:scientificNameAuthorship')
    locality = xmlmap.StringField('dwc:locality')
    location_remarks = xmlmap.StringField('dwc:locationRemarks')
    municipality = xmlmap.StringField('dwc:municipality')
    county = xmlmap.StringField('dwc:county')
    state_province = xmlmap.StringField('dwc:stateProvince')
    country = xmlmap.StringField('dwc:country')
    geodetic_datum = xmlmap.StringField('dwc:geodeticDatum')
    decimal_latitude = xmlmap.StringField('dwc:decimalLatitude')
    decimal_longitude = xmlmap.StringField('dwc:decimalLongitude')
    coordinate_uncertainty_in_meters = xmlmap.StringField('dwc:coordinateUncertaintyInMeters')
    verbatim_coordinates = xmlmap.StringField('dwc:verbatimCoordinates')
    habitat = xmlmap.StringField('dwc:habitat')
    identification_id = xmlmap.StringField('dwc:identificationID')
    collection_id = xmlmap.StringField('dwc:collectionID')
    collection_code = xmlmap.StringField('dwc:collectionCode')
    year = xmlmap.StringField('dwc:year')
    month = xmlmap.StringField('dwc:month')
    day = xmlmap.StringField('dwc:day')
    occurrence_id = xmlmap.StringField('dwc:occurrenceID')
    occurrence_remarks = xmlmap.StringField('dwc:occurrenceRemarks')
    start_day_of_year = xmlmap.StringField('dwc:startDayOfYear')
    end_day_of_year = xmlmap.StringField('dwc:endDayOfYear')
    institution_code = xmlmap.StringField('dwc:institutionCode')


class SimpleDarwinRecordSet(xmlmap.XmlObject):
    ROOT_NAME = 'SimpleDarwinRecordSet'
    ROOT_NS = XMLNS
    ROOT_NAMESPACES = {'sdr': XMLNS,
                       'dc': DCNS,
                       'dwc': DWCNS,
                       'xsi': XSINS}
    XSD_SCHEMA = 'http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd'
    xsi_schema_location = xmlmap.StringField('@xsi:schemaLocation')

    simple_darwin_record = xmlmap.NodeField('sdr:SimpleDarwinRecord', SimpleDarwinRecord)


def make_simple_darwin_record():
    sdr = SimpleDarwinRecord()
    sdr.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdr


def make_simple_darwin_record_set():
    sdrs = SimpleDarwinRecordSet()
    sdrs.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdrs
