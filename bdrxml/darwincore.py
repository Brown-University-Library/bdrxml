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
    event_id = xmlmap.StringField('dwc:eventID')
    parent_event_id = xmlmap.StringField('dwc:parentEventID')
    field_number = xmlmap.StringField('dwc:fieldNumber')
    event_date = xmlmap.StringField('dwc:eventDate')
    verbatim_event_date = xmlmap.StringField('dwc:verbatimEventDate')
    event_time = xmlmap.StringField('dwc:eventTime')
    start_day_of_year = xmlmap.StringField('dwc:startDayOfYear')
    end_day_of_year = xmlmap.StringField('dwc:endDayOfYear')
    year = xmlmap.StringField('dwc:year')
    month = xmlmap.StringField('dwc:month')
    day = xmlmap.StringField('dwc:day')
    field_notes = xmlmap.StringField('dwc:fieldNotes')
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
    georeferenced_by = xmlmap.StringField('dwc:georeferencedBy')
    georeferenced_date = xmlmap.StringField('dwc:georeferencedDate')
    georeference_sources = xmlmap.StringField('dwc:georeferenceSources')
    georeference_protocol = xmlmap.StringField('dwc:georeferenceProtocol')
    georeference_remarks = xmlmap.StringField('dwc:georeferenceRemarks')
    georeference_verification_status = xmlmap.StringField('dwc:georeferenceVerificationStatus')
    decimal_latitude = xmlmap.StringField('dwc:decimalLatitude')
    decimal_longitude = xmlmap.StringField('dwc:decimalLongitude')
    coordinate_uncertainty_in_meters = xmlmap.StringField('dwc:coordinateUncertaintyInMeters')
    verbatim_coordinates = xmlmap.StringField('dwc:verbatimCoordinates')
    minimum_elevation_in_meters = xmlmap.StringField('dwc:minimumElevationInMeters')
    maximum_elevation_in_meters = xmlmap.StringField('dwc:maximumElevationInMeters')
    verbatim_elevation = xmlmap.StringField('dwc:verbatimElevation')
    minimum_depth_in_meters = xmlmap.StringField('dwc:minimumDepthInMeters')
    maximum_depth_in_meters = xmlmap.StringField('dwc:maximumDepthInMeters')
    verbatim_depth = xmlmap.StringField('dwc:verbatimDepth')
    habitat = xmlmap.StringField('dwc:habitat')
    identification_id = xmlmap.StringField('dwc:identificationID')
    collection_id = xmlmap.StringField('dwc:collectionID')
    collection_code = xmlmap.StringField('dwc:collectionCode')
    institution_code = xmlmap.StringField('dwc:institutionCode')
    dynamic_properties = xmlmap.StringField('dwc:dynamicProperties')
    data_generalizations = xmlmap.StringField('dwc:dataGeneralizations')
    information_withheld = xmlmap.StringField('dwc:informationWithheld')
    #Occurrence terms
    occurrence_id = xmlmap.StringField('dwc:occurrenceID')
    catalog_number = xmlmap.StringField('dwc:catalogNumber')
    record_number = xmlmap.StringField('dwc:recordNumber')
    recorded_by = xmlmap.StringField('dwc:recordedBy')
    individual_count = xmlmap.StringField('dwc:individualCount')
    organism_quantity = xmlmap.StringField('dwc:organismQuantity')
    organism_quantity_type = xmlmap.StringField('dwc:organismQuantityType')
    sex = xmlmap.StringField('dwc:sex')
    life_stage = xmlmap.StringField('dwc:lifeStage')
    reproductive_condition = xmlmap.StringField('dwc:reproductiveCondition')
    behavior = xmlmap.StringField('dwc:behavior')
    establishment_means = xmlmap.StringField('dwc:establishmentMeans')
    occurrence_status = xmlmap.StringField('dwc:occurrenceStatus')
    preparations = xmlmap.StringField('dwc:preparations')
    disposition = xmlmap.StringField('dwc:disposition')
    associated_media = xmlmap.StringField('dwc:associatedMedia')
    associated_references = xmlmap.StringField('dwc:associatedReferences')
    associated_sequences = xmlmap.StringField('dwc:associatedSequences')
    associated_taxa = xmlmap.StringField('dwc:associatedTaxa')
    other_catalog_numbers = xmlmap.StringField('dwc:otherCatalogNumbers')
    occurrence_remarks = xmlmap.StringField('dwc:occurrenceRemarks')


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
