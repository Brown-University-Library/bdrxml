# coding: utf-8
from __future__ import unicode_literals
from eulxml import xmlmap
from eulxml.xmlmap import StringField as SF

from . import mods
from . import darwincore
from .rights import Rights, RIGHTS_NAMESPACE
from .irMetadata import IR, IR_NAMESPACE

METS_NAMESPACE = 'http://www.loc.gov/METS/'
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'

class Common(xmlmap.XmlObject):
    "METS class with namespace declaration common to all METS XmlObjects."
    ROOT_NS = METS_NAMESPACE
    ROOT_NAME = 'mets'
    ROOT_NAMESPACES = {
                       'METS': METS_NAMESPACE,
                       'rights': RIGHTS_NAMESPACE,
                       #For now we are assuming the METS will include a MODS.
                       'mods': mods.MODS_NAMESPACE,
                       'sdr': 'http://rs.tdwg.org/dwc/xsd/simpledarwincore/',
                       'ir': IR_NAMESPACE,
                       'xlink': XLINK_NAMESPACE,
                       'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                       'xs': 'http://www.w3.org/2001/XMLSchema',
                       }

class File(Common):
    ROOT_NAME = 'file'
    id = SF('@ID')
    mimetype = SF('@MIMETYPE')
    seq = SF('@SEQ')
    groupid = SF('@GROUPID')
    admid = SF('@ADMID')
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
    
class StructMap( Common ):
    ROOT_NAME = 'structMap'
    
class MdWrap(Common):
    type = SF('@MDTYPE')
    xml = xmlmap.NodeField('METS:xmlData', xmlmap.XmlObject)
    mods = xmlmap.NodeField('METS:xmlData/mods:mods', xmlmap.XmlObject)  

class BDRMets(Common):
    """BDRMets class."""
    ROOT_NAME = 'mets'
    XSD_SCHEMA = 'http://www.loc.gov/standards/mets/mets.xsd'
    pid = xmlmap.StringField('@OBJID')
    mdwrap = xmlmap.NodeField('METS:dmdSec[@ID="DM1"]/METS:mdWrap', MdWrap)
    mods = xmlmap.NodeField('METS:dmdSec[@ID="DM1"]/METS:mdWrap[@MDTYPE="MODS"]/METS:xmlData/mods:mods', mods.Mods)
    dwc = xmlmap.NodeField('METS:dmdSec[@ID="DM2"]/METS:mdWrap[@MDTYPE="OTHER"]/METS:xmlData/sdr:SimpleDarwinRecordSet', darwincore.SimpleDarwinRecordSet)
    ir = xmlmap.NodeField('METS:dmdSec[@ID="DM3"]/METS:mdWrap[@MDTYPE="OTHER"][@OTHERMDTYPE="IR"]/METS:xmlData/ir:irData', IR)
    rights = xmlmap.NodeField('METS:amdSec/METS:rightsMD[@ID="RMD1"]/METS:mdWrap[@LABEL="RIGHTSMD"][@MDTYPE="OTHER"]/METS:xmlData/rights:RightsDeclarationMD', Rights)
    filesec = xmlmap.NodeField('METS:fileSec', FileSec)
    structmap = xmlmap.NodeField( 'METS:structMap/METS:div', StructMap )  # not used but required for valid mets
    schema_location = SF('@xsi:schemaLocation', 'self')

def make_mets():
    """
    Helper to initialize a BDR Mets.
    """
    m = BDRMets()
    m.schema_location = 'http://www.loc.gov/METS/ http://www.loc.gov/standards/mets/mets.xsd http://www.loc.gov/standards/mods/v3/ http://www.loc.gov/standards/mods/v3/mods-3-3.xsd'
    return m
