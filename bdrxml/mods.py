# coding: utf-8
from __future__ import unicode_literals
import re
import unicodedata
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeListField, NodeField
#import everything from eulxml.xmlmap.mods because clients have to use a lot of
#   those classes, and we're just overriding a few of them here.
from eulxml.xmlmap.mods import *

XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_LOCATION = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd'

class PlaceTerm(Common):
    ROOT_NAME = 'placeTerm'
    type = SF('@type')
    authority = SF('@authority')
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    text = SF('text()')

class Place(Common):
    ROOT_NAME = 'place'
    place_terms = NodeListField('mods:placeTerm', PlaceTerm)

class OriginInfo(OriginInfo):
    label = SF('@displayLabel')
    places = NodeListField('mods:place', Place)


class Collection(RelatedItem):
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')


class PhysicalDescriptionForm(Common):
    ROOT_NAME = 'form'
    authority = SF('@authority')
    type = SF('@type')
    text = SF('text()')

class PhysicalDescription(PhysicalDescription):
    digital_origin = SF('mods:digitalOrigin')
    note = SF('mods:note')
    forms = NodeListField('mods:form', PhysicalDescriptionForm)


class PhysicalLocation(Common):
    ROOT_NAME = 'physicalLocation'
    authority = SF('@authority')
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    text = SF('text()')


class CopyInformation(Common):
    ROOT_NAME = 'copyInformation'
    notes = NodeListField('mods:note', Note)


class HoldingSimple(Common):
    ROOT_NAME = 'holdingSimple'
    copy_information = NodeListField('mods:copyInformation', CopyInformation)


class Location(Location):
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


class Topic(Common):
    ROOT_NAME = 'topic'
    authority = SF('@authority')
    text = SF('text()')


class Subject(Subject):
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


class Classification(Common):
    ROOT_NAME = 'classification'
    label = SF('@displayLabel')
    authority = SF('@authority')
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')
    text = SF('text()')


class Genre(Genre):
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')


class TargetAudience(Common):
    ROOT_NAME = 'targetAudience'
    authority = SF('@authority')
    text = SF('text()')


class RecordInfo(RecordInfo):
    record_identifier_list = NodeListField('mods:recordIdentifier', RecordIdentifier)


class Role(Role):
    authority_uri = SF('mods:roleTerm/@authorityURI')
    value_uri = SF('mods:roleTerm/@valueURI')


class Name(Name):
    roles = xmlmap.NodeListField('mods:role', Role)
    authority_uri = SF('@authorityURI')
    value_uri = SF('@valueURI')


class BaseMods(BaseMods):
    classifications = NodeListField('mods:classification', Classification)
    #override eulxml origin_info, because we add a displayLabel
    origin_info = NodeField('mods:originInfo', OriginInfo)
    #override eulxml subjects so we can add hierarchical_geographic to subject
    subjects = NodeListField('mods:subject', Subject)
    physical_description = NodeField('mods:physicalDescription', PhysicalDescription)
    locations = NodeListField('mods:location', Location)
    genres = NodeListField('mods:genre', Genre)
    target_audiences = NodeListField('mods:targetAudience', TargetAudience)
    record_info_list = NodeListField('mods:recordInfo', RecordInfo)
    names = xmlmap.NodeListField('mods:name', Name)


class RelatedItem(BaseMods):
    ROOT_NAME = 'relatedItem'
    type = xmlmap.SchemaField("@type", 'relatedItemTypeAttributeDefinition')
    label = xmlmap.StringField('@displayLabel')


class Mods(BaseMods):
    """Map mods fields - just where we override MODSv34
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    ROOT_NAME = 'mods'
    XSD_SCHEMA = MODSv34_SCHEMA
    Common.ROOT_NAMESPACES['xlink'] = XLINK_NAMESPACE
    Common.ROOT_NAMESPACES['xsi'] = XSI_NAMESPACE
    xsi_schema_location = SF('@xsi:schemaLocation')

    #deprecated - should use title_info_list from eulxml instead
    title_info = NodeListField('mods:titleInfo', TitleInfo)
    #Add a commonly used related item
    collection = NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)
    related_items = xmlmap.NodeListField('mods:relatedItem', RelatedItem)


def make_mods():
    """Helper that returns Mods object."""
    m = Mods()
    m.xsi_schema_location = XSI_LOCATION
    return m

