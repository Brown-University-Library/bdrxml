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

    type = xmlmap.StringField('dc:type')
    modified = xmlmap.StringField('dc:modified')
    language = xmlmap.StringField('dc:language')
    rights = xmlmap.StringField('dc:rights')
    rights_holder = xmlmap.StringField('dc:rightsHolder')
    bibliographic_citation = xmlmap.StringField('dc:bibliographicCitation')
    references = xmlmap.StringField('dc:references')
    basis_of_record = xmlmap.StringField('dwc:basisOfRecord')
    catalog_number = xmlmap.StringField('dwc:catalogNumber')
    recorded_by = xmlmap.StringField('dwc:recordedBy')
    individual_id = xmlmap.StringField('dwc:individualID')
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
    county = xmlmap.StringField('dwc:county')
    state_province = xmlmap.StringField('dwc:stateProvince')
    country = xmlmap.StringField('dwc:country')
    habitat = xmlmap.StringField('dwc:habitat')
    identification_id = xmlmap.StringField('dwc:identificationID')


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


class SimpleDarwinRecordIndexer(object):

    def __init__(self, dwc):
        self.dwc = dwc

    def index_data(self):
        fields = ['catalog_number', 'recorded_by', 'individual_id', 'event_date', 'verbatim_event_date',
                'scientific_name', 'higher_classification', 'kingdom', 'phylum', 'class_', 'order',
                'family', 'genus', 'specific_epithet', 'infraspecific_epithet', 'taxon_rank', 'accepted_name_usage',
                'scientific_name_authorship', 'county', 'state_province', 'country', 'habitat', 'identification_id']
        data = {}
        for field in fields:
            if getattr(self.dwc, field):
                if field.endswith(u'_'):
                    field_name = u'dwc_%sssi' % field
                else:
                    field_name = u'dwc_%s_ssi' % field
                data[field_name] =  u'%s' % getattr(self.dwc, field)
        return data


def make_simple_darwin_record():
    sdr = SimpleDarwinRecord()
    sdr.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdr


def make_simple_darwin_record_set():
    sdrs = SimpleDarwinRecordSet()
    sdrs.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdrs
