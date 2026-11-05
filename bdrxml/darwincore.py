import os
from typing import TYPE_CHECKING

from lxml import etree
from neuxml import xmlmap
from neuxml.xmlmap import dc

XMLNS = 'http://rs.tdwg.org/dwc/xsd/simpledarwincore/'
DCNS = 'http://purl.org/dc/terms/'
DWCNS = 'http://rs.tdwg.org/dwc/terms/'
XSINS = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_SCHEMA_LOCATION = 'http://rs.tdwg.org/dwc/xsd/simpledarwincore/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(CURRENT_DIR, 'schemas')


def get_schema_validation_errors(schema_name, lxml_node):
    with open(os.path.join(SCHEMA_DIR, schema_name), 'rb') as f:
        xmlschema = etree.XMLSchema(etree.parse(f))
        if xmlschema.validate(lxml_node):
            return []
        else:
            return xmlschema.error_log


BASE_CLASS_MEMBERS: dict[str, object] = dict(
    ROOT_NAME = 'SimpleDarwinRecord',
    XSD_SCHEMA = None,
    ROOT_NAMESPACES = {}
)

DWC_TERMS = [
    'dc:type',
    'dc:modified',
    'dc:language',
    'dc:rights', #deprecated - probably use license instead
    'dc:accessRights',
    'dc:license',
    'dc:rightsHolder',
    'dc:bibliographicCitation',
    'dc:references',
    'dwc:typeStatus',
    'dwc:basisOfRecord',
    #Event terms
    'dwc:eventID',
    'dwc:parentEventID',
    'dwc:fieldNumber',
    'dwc:eventDate',
    'dwc:eventTime',
    'dwc:startDayOfYear',
    'dwc:endDayOfYear',
    'dwc:year',
    'dwc:month',
    'dwc:day',
    'dwc:verbatimEventDate',
    'dwc:habitat',
    'dwc:samplingProtocol',
    'dwc:samplingEffort',
    'dwc:sampleSizeValue',
    'dwc:sampleSizeUnit',
    'dwc:fieldNotes',
    'dwc:eventRemarks',
    'dwc:scientificName',
    'dwc:higherClassification',
    'dwc:kingdom',
    'dwc:phylum',
    'dwc:class',
    'dwc:order',
    'dwc:family',
    'dwc:genus',
    'dwc:specificEpithet',
    'dwc:infraspecificEpithet',
    'dwc:taxonRank',
    'dwc:taxonID',
    'dwc:acceptedNameUsage',
    'dwc:scientificNameAuthorship',
    'dwc:locality',
    'dwc:locationRemarks',
    'dwc:municipality',
    'dwc:county',
    'dwc:stateProvince',
    'dwc:country',
    'dwc:geodeticDatum',
    'dwc:georeferencedBy',
    'dwc:georeferencedDate',
    'dwc:georeferenceSources',
    'dwc:georeferenceProtocol',
    'dwc:georeferenceRemarks',
    'dwc:georeferenceVerificationStatus',
    'dwc:decimalLatitude',
    'dwc:decimalLongitude',
    'dwc:coordinateUncertaintyInMeters',
    'dwc:verbatimCoordinates',
    'dwc:minimumElevationInMeters',
    'dwc:maximumElevationInMeters',
    'dwc:verbatimElevation',
    'dwc:minimumDepthInMeters',
    'dwc:maximumDepthInMeters',
    'dwc:verbatimDepth',
    'dwc:identificationID',
    'dwc:collectionID',
    'dwc:collectionCode',
    'dwc:institutionCode',
    'dwc:dynamicProperties',
    'dwc:dataGeneralizations',
    'dwc:informationWithheld',
    'dwc:occurrenceID',
    'dwc:catalogNumber',
    'dwc:recordNumber',
    'dwc:recordedBy',
    'dwc:individualCount',
    'dwc:organismQuantity',
    'dwc:organismQuantityType',
    'dwc:sex',
    'dwc:lifeStage',
    'dwc:reproductiveCondition',
    'dwc:behavior',
    'dwc:establishmentMeans',
    'dwc:occurrenceStatus',
    'dwc:preparations',
    'dwc:disposition',
    'dwc:associatedMedia',
    'dwc:associatedReferences',
    'dwc:associatedSequences',
    'dwc:associatedTaxa',
    'dwc:otherCatalogNumbers',
    'dwc:occurrenceRemarks',
]

def _get_attribute_name_from_term(term):
    term = term.replace('dwc:', '').replace('dc:', '')
    attr = ''
    for char in term:
        if char.isupper():
            if attr[-1] == 'i' and char == 'D':
                attr = '%s%s' % (attr, char.lower())
            else:
                attr = '%s_%s' % (attr, char.lower())
        else:
            attr = '%s%s' % (attr, char)
    if attr in ['type', 'class']:
        attr = '%s_' % attr
    return attr


def _get_class_members():
    class_members = BASE_CLASS_MEMBERS.copy()
    for term in DWC_TERMS:
        attr_name = _get_attribute_name_from_term(term)
        class_members[attr_name] = xmlmap.StringField(term)
    return class_members


class_name = 'SimpleDarwinRecord'
if TYPE_CHECKING:
    class SimpleDarwinRecord(xmlmap.XmlObject):
        type_: str | None
        modified: str | None
        language: str | None
        rights: str | None
        access_rights: str | None
        license: str | None
        rights_holder: str | None
        bibliographic_citation: str | None
        references: str | None
        type_status: str | None
        basis_of_record: str | None
        event_id: str | None
        parent_event_id: str | None
        field_number: str | None
        event_date: str | None
        event_time: str | None
        start_day_of_year: str | None
        end_day_of_year: str | None
        year: str | None
        month: str | None
        day: str | None
        verbatim_event_date: str | None
        habitat: str | None
        sampling_protocol: str | None
        sampling_effort: str | None
        sample_size_value: str | None
        sample_size_unit: str | None
        field_notes: str | None
        event_remarks: str | None
        scientific_name: str | None
        higher_classification: str | None
        kingdom: str | None
        phylum: str | None
        class_: str | None
        order: str | None
        family: str | None
        genus: str | None
        specific_epithet: str | None
        infraspecific_epithet: str | None
        taxon_rank: str | None
        taxon_id: str | None
        accepted_name_usage: str | None
        scientific_name_authorship: str | None
        locality: str | None
        location_remarks: str | None
        municipality: str | None
        county: str | None
        state_province: str | None
        country: str | None
        geodetic_datum: str | None
        georeferenced_by: str | None
        georeferenced_date: str | None
        georeference_sources: str | None
        georeference_protocol: str | None
        georeference_remarks: str | None
        georeference_verification_status: str | None
        decimal_latitude: str | None
        decimal_longitude: str | None
        coordinate_uncertainty_in_meters: str | None
        verbatim_coordinates: str | None
        minimum_elevation_in_meters: str | None
        maximum_elevation_in_meters: str | None
        verbatim_elevation: str | None
        minimum_depth_in_meters: str | None
        maximum_depth_in_meters: str | None
        verbatim_depth: str | None
        identification_id: str | None
        collection_id: str | None
        collection_code: str | None
        institution_code: str | None
        dynamic_properties: str | None
        data_generalizations: str | None
        information_withheld: str | None
        occurrence_id: str | None
        catalog_number: str | None
        record_number: str | None
        recorded_by: str | None
        individual_count: str | None
        organism_quantity: str | None
        organism_quantity_type: str | None
        sex: str | None
        life_stage: str | None
        reproductive_condition: str | None
        behavior: str | None
        establishment_means: str | None
        occurrence_status: str | None
        preparations: str | None
        disposition: str | None
        associated_media: str | None
        associated_references: str | None
        associated_sequences: str | None
        associated_taxa: str | None
        other_catalog_numbers: str | None
        occurrence_remarks: str | None
        xsi_schema_location: str
else:
    SimpleDarwinRecord = type(class_name, (xmlmap.XmlObject,), _get_class_members())


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

    def validation_errors(self):
        '''Use local validation so we're not dependent on HTTP calls and xsd docs staying at the same URL.
        Note: XmlObject.is_valid() looks like this:
                return self.validation_errors() == []
            So, we just need to override validation_errors().
        '''
        return get_schema_validation_errors(schema_name='tdwg_dwc_simple.xsd', lxml_node=self.node)


    if TYPE_CHECKING:
        def create_simple_darwin_record(self) -> None: ...

def make_simple_darwin_record():
    sdr = SimpleDarwinRecord()
    sdr.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdr


def make_simple_darwin_record_set():
    sdrs = SimpleDarwinRecordSet()
    sdrs.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdrs

