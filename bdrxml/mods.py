import re
import unicodedata
from typing import TYPE_CHECKING

from neuxml import xmlmap
from neuxml.xmlmap import NodeField, NodeListField, SchemaField
from neuxml.xmlmap import StringField as SF

#import everything from neuxml.xmlmap.mods because clients have to use a lot of
#   those classes, and we're just overriding a few of them here.
from neuxml.xmlmap.mods import (
    MODS,
    MODS_NAMESPACE,
    MODS_SCHEMA,
    Abstract,
    AccessCondition,
    Common,
    CopyrightDate,
    Date,
    DateCaptured,
    DateCreated,
    DateIssued,
    DateModified,
    DateOther,
    DateValid,
    Identifier,
    MODSv34,
    MODSv34_SCHEMA,
    NamePart,
    Note,
    PartExtent,
    TitleInfo,
    TypedNote,
)
from neuxml.xmlmap.mods import BaseMods as NeuXmlBaseMods
from neuxml.xmlmap.mods import Genre as NeuXmlGenre
from neuxml.xmlmap.mods import Language as NeuXmlLanguage
from neuxml.xmlmap.mods import LanguageTerm as NeuXmlLanguageTerm
from neuxml.xmlmap.mods import Location as NeuXmlLocation
from neuxml.xmlmap.mods import Name as NeuXmlName
from neuxml.xmlmap.mods import OriginInfo as NeuXmlOriginInfo
from neuxml.xmlmap.mods import PartDetail as NeuXmlPartDetail
from neuxml.xmlmap.mods import PhysicalDescription as NeuXmlPhysicalDescription
from neuxml.xmlmap.mods import RecordInfo as NeuXmlRecordInfo
from neuxml.xmlmap.mods import RelatedItem as NeuXmlRelatedItem
from neuxml.xmlmap.mods import Role as NeuXmlRole
from neuxml.xmlmap.mods import Subject as NeuXmlSubject

from .darwincore import get_schema_validation_errors

XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
# XSI_LOCATION = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-7.xsd'
XSI_LOCATION = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-8.xsd'
MODSv35_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-5.xsd"
MODSv37_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-7.xsd"
MODSv38_SCHEMA = "http://www.loc.gov/standards/mods/v3/mods-3-8.xsd"
FAST = 'http://id.worldcat.org/fast'

__all__ = [
    'FAST', 'MODS', 'MODS_NAMESPACE', 'MODS_SCHEMA', 'XLINK_NAMESPACE', 'XSI_LOCATION', 'XSI_NAMESPACE', 'Abstract',
    'AccessCondition', 'BaseMods', 'Classification', 'Collection', 'Common', 'CommonField', 'CopyInformation',
    'CopyrightDate', 'Date', 'DateCaptured', 'DateCreated', 'DateIssued', 'DateModified', 'DateOther', 'DateValid',
    'Genre', 'HierarchicalGeographic', 'HoldingSimple', 'Identifier', 'Language', 'LanguageTerm', 'Location', 'MODSv34',
    'MODSv34_SCHEMA', 'MODSv35_SCHEMA', 'MODSv37_SCHEMA', 'MODSv38_SCHEMA', 'Mods', 'Mods37', 'Name', 'NamePart',
    'Note', 'OriginInfo', 'Part', 'PartDetail', 'PartExtent', 'PhysicalDescription', 'PhysicalDescriptionForm',
    'PhysicalLocation', 'Place', 'PlaceTerm', 'RecordContentSource', 'RecordCreationDate', 'RecordIdentifier',
    'RecordInfo', 'RelatedItem', 'ResourceType', 'Role', 'SubLocation', 'Subject', 'TargetAudience', 'Temporal',
    'TitleInfo', 'Topic', 'TypedNote', 'add_topic', 'make_mods', 'xmlmap',
]


class CommonField(Common):
    '''gives us common parts of an element like authority, authorityURI, valueURI, ...'''
    authority = SF('@authority')
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    text = SF('text()')


class PartDetail(NeuXmlPartDetail):
    caption = SF('mods:caption')


class Part(NeuXmlPartDetail):
    details = NodeListField('mods:detail', PartDetail)


class PlaceTerm(CommonField):
    ROOT_NAME = 'placeTerm'
    type = SF('@type')


class Place(Common):
    ROOT_NAME = 'place'
    place_terms = NodeListField('mods:placeTerm', PlaceTerm)


class OriginInfo(NeuXmlOriginInfo):
    label = SF('@displayLabel')
    places = NodeListField('mods:place', Place)


class Collection(NeuXmlRelatedItem):
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')


class LanguageTerm(NeuXmlLanguageTerm):
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')


class Language(NeuXmlLanguage):
    terms = NodeListField('mods:languageTerm', LanguageTerm)


class PhysicalDescriptionForm(CommonField):
    ROOT_NAME = 'form'
    type = SF('@type')


class PhysicalDescription(NeuXmlPhysicalDescription):
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


class Location(NeuXmlLocation):
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


class Subject(NeuXmlSubject):
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


class Genre(NeuXmlGenre):
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


class RecordInfo(NeuXmlRecordInfo):
    record_identifier_list = NodeListField('mods:recordIdentifier', RecordIdentifier)
    record_creation_date = NodeField('mods:recordCreationDate', RecordCreationDate)
    record_content_source = NodeField('mods:recordContentSource', RecordContentSource)


class Role(NeuXmlRole):
    authority_uri = SF('mods:roleTerm/@authorityURI')
    value_uri = SF('mods:roleTerm/@valueURI')


class Name(NeuXmlName):
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


class BaseMods(NeuXmlBaseMods):
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
    """Map mods fields - just where we override MODSv34 from neuxml
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    ROOT_NAME = 'mods'
    XSD_SCHEMA = MODSv38_SCHEMA
    Common.ROOT_NAMESPACES['xlink'] = XLINK_NAMESPACE
    Common.ROOT_NAMESPACES['xsi'] = XSI_NAMESPACE
    xsi_schema_location = SF('@xsi:schemaLocation')

    #deprecated - should use title_info_list from neuxml instead
    title_info = NodeListField('mods:titleInfo', TitleInfo)
    #Add a commonly used related item
    collection = NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)
    related_items = xmlmap.NodeListField('mods:relatedItem', RelatedItem)

    def validation_errors(self):
        '''see notes on SimpleDarwinRecordSet.validation_errors()'''
        schema_name = 'mods-3-7.xsd' if self.XSD_SCHEMA == MODSv37_SCHEMA else 'mods-3-8.xsd'
        return get_schema_validation_errors(schema_name=schema_name, lxml_node=self.node)
    

    if TYPE_CHECKING:
        def create_origin_info(self) -> None: ...

class Mods37(Mods):
    """Retains MODS 3.7 for applications that require that schema version."""

    XSD_SCHEMA = MODSv37_SCHEMA


def make_mods(*, schema_version: str = '3.8') -> Mods:
    """
    Creates a MODS record for a supported bundled schema, defaulting to 3.8.
    Called by: applications creating MODS records
    """
    if schema_version == '3.7':
        m = Mods37(xsi_schema_location=f'http://www.loc.gov/mods/v3 {MODSv37_SCHEMA}')
    elif schema_version == '3.8':
        m = Mods(xsi_schema_location=XSI_LOCATION)
    else:
        raise ValueError(f'Unsupported MODS schema version: {schema_version}')
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

