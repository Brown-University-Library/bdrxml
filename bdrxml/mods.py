import re
import unicodedata

from .darwincore import get_schema_validation_errors
from eulxml import xmlmap
from eulxml.xmlmap import StringField as SF, SchemaField, NodeListField, NodeField

#import everything from eulxml.xmlmap.mods because clients have to use a lot of
#   those classes, and we're just overriding a few of them here.
from eulxml.xmlmap.mods import *
from eulxml.xmlmap.mods import BaseMods as EulXmlBaseMods
from eulxml.xmlmap.mods import Common, Date, Note, TitleInfo
from eulxml.xmlmap.mods import Genre as EulXmlGenre
from eulxml.xmlmap.mods import Language as EulXmlLanguage
from eulxml.xmlmap.mods import LanguageTerm as EulXmlLanguageTerm
from eulxml.xmlmap.mods import Location as EulXmlLocation
from eulxml.xmlmap.mods import Name as EulXmlName
from eulxml.xmlmap.mods import OriginInfo as EulXmlOriginInfo
from eulxml.xmlmap.mods import PartDetail as EulXmlPartDetail
from eulxml.xmlmap.mods import PhysicalDescription as EulXmlPhysicalDescription
from eulxml.xmlmap.mods import RecordInfo as EulXmlRecordInfo
from eulxml.xmlmap.mods import RelatedItem as EulXmlRelatedItem
from eulxml.xmlmap.mods import Role as EulXmlRole
from eulxml.xmlmap.mods import Subject as EulXmlSubject


XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
# XSI_LOCATION = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-7.xsd'
XSI_LOCATION = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-8.xsd'
MODSv35_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-5.xsd"
MODSv37_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-7.xsd"
MODSv38_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-8.xsd"
FAST = 'http://id.worldcat.org/fast'


class CommonField(Common):
    '''gives us common parts of an element like authority, authorityURI, valueURI, ...'''
    authority = SF('@authority')
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    text = SF('text()')


class PartDetail(EulXmlPartDetail):
    caption = SF('mods:caption')


class Part(EulXmlPartDetail):
    details = NodeListField('mods:detail', PartDetail)


class PlaceTerm(CommonField):
    ROOT_NAME = 'placeTerm'
    type = SF('@type')


class Place(Common):
    ROOT_NAME = 'place'
    place_terms = NodeListField('mods:placeTerm', PlaceTerm)


class OriginInfo(EulXmlOriginInfo):
    label = SF('@displayLabel')
    places = NodeListField('mods:place', Place)


class Collection(EulXmlRelatedItem):
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')


class LanguageTerm(EulXmlLanguageTerm):
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')


class Language(EulXmlLanguage):
    terms = NodeListField('mods:languageTerm', LanguageTerm)


class PhysicalDescriptionForm(CommonField):
    ROOT_NAME = 'form'
    type = SF('@type')


class PhysicalDescription(EulXmlPhysicalDescription):
    digital_origin = SF('mods:digitalOrigin')
    note = SF('mods:note')
    forms = NodeListField('mods:form', PhysicalDescriptionForm)


class PhysicalLocation(CommonField):
    ROOT_NAME = 'physicalLocation'


class SubLocation(Common):
    text = SF('text()')
    lang = SF('@lang')
    script = SF('@script')
    transliteration = SF('@transliteration')


class CopyInformation(Common):
    ROOT_NAME = 'copyInformation'
    notes = NodeListField('mods:note', Note)
    sublocations = NodeListField('mods:subLocation', SubLocation)


class HoldingSimple(Common):
    ROOT_NAME = 'holdingSimple'
    copy_information = NodeListField('mods:copyInformation', CopyInformation)


class Location(EulXmlLocation):
    physical = NodeField('mods:physicalLocation', PhysicalLocation)
    holding_simple = NodeField('mods:holdingSimple', HoldingSimple)


class HierarchicalGeographic(Common):
    ROOT_NAME = 'hierarchicalGeographic'
    continent = SF('mods:continent')
    country = SF('mods:country')
    province = SF('mods:province')
    region = SF('mods:region')
    state = SF('mods:state')
    territory = SF('mods:territory')
    county = SF('mods:county')
    city = SF('mods:city')
    city_section = SF('mods:citySection')
    island = SF('mods:island')
    extraterrestrial_area = SF('mods:extraterrestrialArea')


class Temporal(Common):
    ROOT_NAME = 'temporal'
    encoding = SF('@encoding')
    text = SF('text()')


class Topic(CommonField):
    ROOT_NAME = 'topic'


class Subject(EulXmlSubject):
    label = SF('@displayLabel')
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    topic_list = NodeListField('mods:topic', Topic)
    hierarchical_geographic = NodeField('mods:hierarchicalGeographic', HierarchicalGeographic)
    temporal_list = NodeListField('mods:temporal', Temporal)


class RecordIdentifier(Common):
    ROOT_NAME = 'recordIdentifier'
    source = SF('@source')
    text = SF('text()')


class Classification(CommonField):
    ROOT_NAME = 'classification'
    label = SF('@displayLabel')


class Genre(EulXmlGenre):
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    type = SF('@type')


class TargetAudience(Common):
    ROOT_NAME = 'targetAudience'
    authority = SF('@authority')
    text = SF('text()')


class RecordCreationDate(Date):
    ROOT_NAME = 'recordCreationDate'


class RecordContentSource(CommonField):
    ROOT_NAME = 'recordContentSource'


class RecordInfo(EulXmlRecordInfo):
    record_identifier_list = NodeListField('mods:recordIdentifier', RecordIdentifier)
    record_creation_date = NodeField('mods:recordCreationDate', RecordCreationDate)
    record_content_source = NodeField('mods:recordContentSource', RecordContentSource)


class Role(EulXmlRole):
    authority_uri = SF('mods:roleTerm/@authorityURI')
    value_uri = SF('mods:roleTerm/@valueURI')


class Name(EulXmlName):
    roles = NodeListField('mods:role', Role)
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')


class ResourceType(Common):
    ROOT_NAME = 'typeOfResource'
    authority = SF('@authority')
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    label = SF('@displayLabel')
    text = SF('text()')


class BaseMods(EulXmlBaseMods):
    classifications = NodeListField('mods:classification', Classification)
    origin_info = NodeField('mods:originInfo', OriginInfo)
    subjects = NodeListField('mods:subject', Subject)
    physical_description = NodeField('mods:physicalDescription', PhysicalDescription)
    languages = NodeListField('mods:language', Language)
    locations = NodeListField('mods:location', Location)
    genres = NodeListField('mods:genre', Genre)
    target_audiences = NodeListField('mods:targetAudience', TargetAudience)
    record_info_list = NodeListField('mods:recordInfo', RecordInfo)
    names = NodeListField('mods:name', Name)
    parts = NodeListField('mods:part', Part)
    resource_type = NodeField('mods:typeOfResource', ResourceType)
    resource_types = NodeListField('mods:typeOfResource', ResourceType)


class RelatedItem(BaseMods):
    ROOT_NAME = 'relatedItem'
    type = SchemaField("@type", 'relatedItemTypeAttributeDefinition')
    label = SF('@displayLabel')


class Mods(BaseMods):
    """Map mods fields - just where we override MODSv34 from eulxml
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    ROOT_NAME = 'mods'
    # XSD_SCHEMA = MODSv37_SCHEMA
    XSD_SCHEMA = MODSv38_SCHEMA
    Common.ROOT_NAMESPACES['xlink'] = XLINK_NAMESPACE
    Common.ROOT_NAMESPACES['xsi'] = XSI_NAMESPACE
    xsi_schema_location = SF('@xsi:schemaLocation')

    #deprecated - should use title_info_list from eulxml instead
    title_info = NodeListField('mods:titleInfo', TitleInfo)
    #Add a commonly used related item
    collection = NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)
    related_items = xmlmap.NodeListField('mods:relatedItem', RelatedItem)

    def validation_errors(self):
        '''see notes on SimpleDarwinRecordSet.validation_errors()'''
        #return get_schema_validation_errors(schema_name='mods-3-7.xsd', lxml_node=self.node)
        return get_schema_validation_errors(schema_name='mods-3-8.xsd', lxml_node=self.node)
    

def make_mods():
    """Helper that returns Mods object."""
    m = Mods()
    m.xsi_schema_location = XSI_LOCATION
    return m


def _fast_uris_equal(uri1, uri2):
    if uri1 == uri2:
        return True
    uri1 = uri1.rstrip('/')
    uri2 = uri2.rstrip('/')
    root1, value1 = uri1.rsplit('/', maxsplit=1)
    root2, value2 = uri2.rsplit('/', maxsplit=1)
    if root1 == root2 and int(value1) == int(value2):
        return True
    return False


def add_topic(mods_obj, topic, label=None, fast_uri=None):
    #find or create subject we're working with
    s = None
    for subject in mods_obj.subjects:
        if subject.topic == topic:
            if (subject.label and subject.label != label)\
                    or (subject.value_uri and not _fast_uris_equal(subject.value_uri, fast_uri)):
                #existing subject is incompatible with what we're trying to add
                raise Exception('mods object already has topic "%s"' % topic)
            else:
                s = subject
    if not s:
        s = Subject(topic=topic)
        mods_obj.subjects.append(s)
    #now set any missing info on the subject
    if label and not s.label:
        s.label = label
    if fast_uri and not s.value_uri:
        s.authority = 'fast'
        s.authority_uri = FAST
        s.value_uri = fast_uri

