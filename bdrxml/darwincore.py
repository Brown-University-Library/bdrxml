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

    dwc_scientific_name = xmlmap.StringField('dwc:scientificName')
    dwc_higher_classification = xmlmap.StringField('dwc:higherClassification')
    dwc_kingdom = xmlmap.StringField('dwc:kingdom')
    dwc_phylum = xmlmap.StringField('dwc:phylum')
    dwc_class = xmlmap.StringField('dwc:class')
    dwc_order = xmlmap.StringField('dwc:order')
    dwc_family = xmlmap.StringField('dwc:family')
    dwc_genus = xmlmap.StringField('dwc:genus')


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


def make_simple_darwin_record():
    sdr = SimpleDarwinRecord()
    sdr.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdr


def make_simple_darwin_record_set():
    sdrs = SimpleDarwinRecordSet()
    sdrs.xsi_schema_location = XSI_SCHEMA_LOCATION
    return sdrs