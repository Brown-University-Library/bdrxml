from eulxml import xmlmap
from eulxml.xmlmap import XmlObject
from eulxml.xmlmap import StringField as SF

MODS_NAMESPACE = 'http://www.loc.gov/mods/v3'
MODS_SCHEMA = 'http://www.loc.gov/standards/mods/v3/mods-3-3.xsd'

class Common(XmlObject):
    ROOT_NAMESPACES = {
               'mods': MODS_NAMESPACE,
               'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
               }
    ROOT_NS = MODS_NAMESPACE
    XSD_SCHEMA = MODS_SCHEMA

class Collection(Common):
    ROOT_NAME = 'relatedItem'
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')
    
class PersonalName(Common):
    ROOT_NAME = 'name'
    namePart = SF('mods:namePart')
    years = SF('mods:namePart[@type="date"]')
    role = SF('mods:role/mods:roleTerm')

class CorporateName(Common):
    ROOT_NAME = 'name'
    namePart = SF('mods:namePart')
    #years = SF('mods:namePart[@type="date"]')
    role = SF('mods:role/mods:roleTerm')

class Subject(Common):
    ROOT_NAME = 'subject'
    topic = SF('mods:topic')

class LocalTopic(Common):
    ROOT_NAME = 'subject'
    topic = SF('mods:topic[@type="local"]')

class Mods(Common):
    """Map mods fields."""
    ROOT_NAME = 'mods'
    schema_location = xmlmap.StringField('@xsi:schemaLocation')
    id = SF('@ID')
    title = SF('mods:titleInfo/mods:title')
    publisher = SF('mods:originInfo/mods:publisher')
    language_code = xmlmap.StringField('mods:language/mods:languageTerm[@type="code"]')
    abstract = SF('mods:abstract')
    extent = SF('mods:physicalDescription/mods:extent')
    collection = xmlmap.NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)
    genre = SF('mods:genre')
    personal_name = xmlmap.NodeListField('mods:name[@type="personal"]', PersonalName)
    corporate_name = xmlmap.NodeListField('mods:name[@type="corporate"]', CorporateName)
    created = SF('mods:originInfo/mods:dateCreated')
    local_topic = xmlmap.NodeListField('mods:subject', LocalTopic)
    

def make_mods():
    """
    Helper that sets the XSD and returns Mods object.
    """
    m = Mods()
    return m