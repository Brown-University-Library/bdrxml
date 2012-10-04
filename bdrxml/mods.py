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
    """Map mods fields.
    
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    ROOT_NAME = 'mods'
    id = SF('@ID')
    schema_location = SF('mods:mods/@xsi:schemaLocation')
    #1 titleInfo
    title = SF('mods:titleInfo/mods:title')
    #2 name
    personal_name = xmlmap.NodeListField('mods:name[@type="personal"]', PersonalName)
    corporate_name = xmlmap.NodeListField('mods:name[@type="corporate"]', CorporateName)
    #3 typeOfResource
    typeOfResource = SF('mods:typeOfResource')
    #4 genre
    genre = SF('mods:genre')
    #5 originInfo
    publisher = SF('mods:originInfo/mods:publisher')
    created = SF('mods:originInfo/mods:dateCreated')
    #6 language
    language_code = xmlmap.StringField('mods:language/mods:languageTerm[@type="code"]')
    #7 physicalDescription
    extent = SF('mods:physicalDescription/mods:extent')
    #8 abstract
    abstract = SF('mods:abstract')
    #9 tableOfContents
    #10 targetAudience
    #11 note
    #12 subject
    local_topic = xmlmap.NodeListField('mods:subject', LocalTopic)
    #13 classification
    #14 relatedItem
    collection = xmlmap.NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)
    #15 identifier
    #16 location
    #17 accessCondition
    #18 part
    #19 extension
    #20 recordInfo

def make_mods():
    """
    Helper that sets the XSD and returns Mods object.
    """
    m = Mods()
    #m.schema_location = 'http://www.loc.gov/standards/mods/v3/ http://www.loc.gov/standards/mods/v3/mods-3-3.xsd'
    return m
