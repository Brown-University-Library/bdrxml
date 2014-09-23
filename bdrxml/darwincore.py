from eulxml import xmlmap
from eulxml.xmlmap import dc


XMLNS = 'http://rs.tdwg.org/dwc/xsd/simpledarwincore/'
DCNS = 'http://purl.org/dc/terms/'
DWCNS = 'http://rs.tdwg.org/dwc/terms/'
XSINS = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_SCHEMA_LOCATION = 'http://rs.tdwg.org/dwc/dwcrecord/ http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd'


class SimpleDarwinRecord(dc.DublinCore):
    ROOT_NAME = 'SimpleDarwinRecord'
    ROOT_NS = XMLNS
    ROOT_NAMESPACES = {'sdr': ROOT_NS,
                       'dc': DCNS,
                       'dwc': DWCNS,
                       'xsi': XSINS}
    XSD_SCHEMA = 'http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd'
    xsi_schema_location = xmlmap.StringField('@xsi:schemaLocation')

    dwc_catalog_number = xmlmap.StringField('dwc:catalogNumber')
    dwc_recorded_by = xmlmap.StringField('dwc:recordedBy')
    dwc_individual_id = xmlmap.StringField('dwc:individualID')
    dwc_event_date = xmlmap.StringField('dwc:eventDate')
    dwc_verbatim_event_date = xmlmap.StringField('dwc:verbatimEventDate')
    dwc_scientific_name = xmlmap.StringField('dwc:scientificName')
    dwc_higher_classification = xmlmap.StringField('dwc:higherClassification')
    dwc_kingdom = xmlmap.StringField('dwc:kingdom')
    dwc_phylum = xmlmap.StringField('dwc:phylum')
    dwc_class = xmlmap.StringField('dwc:class')
    dwc_order = xmlmap.StringField('dwc:order')
    dwc_family = xmlmap.StringField('dwc:family')
    dwc_genus = xmlmap.StringField('dwc:genus')
    dwc_specific_epithet = xmlmap.StringField('dwc:specificEpithet')
    dwc_accepted_name_usage = xmlmap.StringField('dwc:acceptedNameUsage')
    dwc_scientific_name_authorship = xmlmap.StringField('dwc:scientificNameAuthorship')
    dwc_county = xmlmap.StringField('dwc:county')
    dwc_state_province = xmlmap.StringField('dwc:stateProvince')
    dwc_country = xmlmap.StringField('dwc:country')
    dwc_habitat = xmlmap.StringField('dwc:habitat')


#this doesn't work yet - see tests
class SimpleDarwinRecordSet(dc.DublinCore):
    ROOT_NAME = 'SimpleDarwinRecordSet'
    ROOT_NS = XMLNS
    ROOT_NAMESPACES = {'sdr': ROOT_NS,
                       'dc': DCNS,
                       'dwc': DWCNS,
                       'xsi': XSINS}
    XSD_SCHEMA = 'http://rs.tdwg.org/dwc/xsd/tdwg_dwc_simple.xsd'
    xsi_schema_location = xmlmap.StringField('@xsi:schemaLocation')

    simple_darwin_record_list = xmlmap.NodeListField('SimpleDarwinRecord', SimpleDarwinRecord)


class SimpleDarwinRecordIndexer(object):

    def __init__(self, dwc):
        self.dwc = dwc

    def index_data(self):
        fields = ['dwc_catalog_number', 'dwc_recorded_by', 'dwc_individual_id', 'dwc_event_date', 'dwc_verbatim_event_date',
                'dwc_scientific_name', 'dwc_higher_classification', 'dwc_kingdom', 'dwc_phylum', 'dwc_class', 'dwc_order',
                'dwc_family', 'dwc_genus', 'dwc_specific_epithet', 'dwc_accepted_name_usage', 'dwc_scientific_name_authorship',
                'dwc_county', 'dwc_state_province', 'dwc_country', 'dwc_habitat']
        data = {}
        for field in fields:
            if hasattr(self.dwc, field):
                data[field] = getattr(self.dwc, field)
        return data


def make_simple_darwin_record():
    sdr = SimpleDarwinRecord()
    sdr.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdr


def make_simple_darwin_record_set():
    sdrs = SimpleDarwinRecordSet()
    sdrs.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdrs