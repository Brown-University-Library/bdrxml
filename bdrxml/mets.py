"""
Making METS for the BDR.

There is minimal support for MODS included.  Should be separated out at some
point.
"""

from eulxml import xmlmap
from eulxml.xmlmap import StringField as SF

from mods import Mods, MODS_NAMESPACE

METS_NAMESPACE = 'http://www.loc.gov/METS/'
RIGHTS_NAMESPACE = 'http://cosimo.stanford.edu/sdr/metsrights/'
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
IR_NAMESPACE = 'http://dl.lib.brown.edu/md/irdata'

class Common(xmlmap.XmlObject):
    "METS class with namespace declaration common to all METS XmlObjects."
    ROOT_NS = METS_NAMESPACE
    ROOT_NAME = 'mets'
    ROOT_NAMESPACES = {
                       'METS': METS_NAMESPACE,
                       'rights': RIGHTS_NAMESPACE,
                       'xlink': XLINK_NAMESPACE,
                       #For now we are assuming the METs will include a Mods.
                       'mods': MODS_NAMESPACE,
                       'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                       'IR': IR_NAMESPACE,
                       }
    schema_location = xmlmap.StringField('@xsi:schemaLocation')

class Context(Common):
    ROOT_NS = RIGHTS_NAMESPACE
    ROOT_NAME = 'Context'
    cclass = SF('@CONTEXTCLASS')
    id = SF('@CONTEXTID')
    delete = SF('rights:Permissions/@DELETE')
    discover = SF('rights:Permissions/@DISCOVER')
    display = SF('rights:Permissions/@DISPLAY')
    modify = SF('rights:Permissions/@MODIFY')
    usertype = SF('rights:UserName/@USERTYPE')
    username = SF('rights:UserName')

class Holder(Common):
    ROOT_NAME = 'RightsHolder'
    context_ids = SF('@CONTEXTIDS')
    name = SF('rights:RightsHolderName')

class Rights(Common):
    ROOT_NAME = 'RightsDeclarationMD'
    category = SF('@RIGHTSCATEGORY')
    holder = xmlmap.NodeField('rights:RightsHolder', Holder)
    #Can't call this context - it's a property inherited from the XMLMap
    ctext = xmlmap.NodeListField('rights:Context', 'self')


class File(Common):
    ROOT_NAME = 'file'
    id = SF('@ID')
    mimetype = SF('@MIMETYPE')
    seq = SF('@SEQ')
    groupid = SF('@GROUPID')
    admid = SF('@TMD1')
    href = SF('METS:FLocat/@xlink:href')
    loctype = SF('METS:FLocat/@LOCTYPE')
    
class FileGrp(Common):
    ROOT_NAME = 'fileGrp'
    id = SF('@ID')
    use = SF('@USE')
    file = xmlmap.NodeListField('METS:file', File)
    
class FileSec(Common):
    ROOT_NAME = 'fileSec'
    filegrp = xmlmap.NodeListField('METS:fileGrp', FileGrp)
    

class IR(Common):
    ROOT_NS = IR_NAMESPACE
    ROOT_NAME = 'irData'
    depositor_name = SF('IR:deposit/IR:depositor/IR:name')
    depositor_email = SF('IR:deposit/IR:depositor/IR:email')
    depositor_eppn = SF('IR:deposit/IR:depositor/IR:eppn')
    date = SF('IR:deposit/IR:date')
    filename = SF('IR:deposit/IR:filename')
    collections_date = SF('IR:collections/IR:date')
    collection = SF('IR:collections/IR:collection')

class BDRMets(Common):
    """BDRMets class."""
    pid = xmlmap.StringField('@OBJID')
    mods = xmlmap.NodeField('METS:dmdSec[@ID="DM1"]/METS:mdWrap[@MDTYPE="MODS"]/METS:xmlData/mods:mods', Mods)
    ir = xmlmap.NodeField('METS:dmdSec[@ID="DM2"]/METS:mdWrap[@MDTYPE="OTHER"][@OTHERMDTYPE="IR"]/METS:xmlData/IR:irData', IR)
    rights = xmlmap.NodeField('METS:amdSec/METS:rightsMD[@ID="RMD1"]/METS:mdWrap[@LABEL="RIGHTSMD"][@MDTYPE="OTHER"]/METS:xmlData/rights:RightsDeclarationMD', Rights)
    filesec = xmlmap.NodeField('METS:mets/METS:fileSec', FileSec)
    

def make_mets():
    """
    Helper to initialize a BDR Mets.
    """
    m = BDRMets()
    m.schema_location = 'http://www.loc.gov/standards/mets/mets.xsd'
    return m