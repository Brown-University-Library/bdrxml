"""
Making rightsMetadata for the BDR.

There is minimal support for MODS included.  Should be separated out at some
point.
"""

from eulxml import xmlmap
from eulxml.xmlmap import XmlObject
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import StringListField as SFL
from eulxml.xmlmap import SimpleBooleanField as BF
RIGHTS_NAMESPACE = 'http://cosimo.stanford.edu/sdr/metsrights/'
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'

class Common(XmlObject):
    ROOT_NAMESPACES = {
               'rights': RIGHTS_NAMESPACE,
               'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
               }
    ROOT_NS = RIGHTS_NAMESPACE
    ROOT_NAME = 'rights'

class Context(Common):
    ROOT_NS = RIGHTS_NAMESPACE
    ROOT_NAME = 'Context'
    cclass = SF('@CONTEXTCLASS')
    id = SF('@CONTEXTID')
    delete = BF('rights:Permissions/@DELETE','true','false')
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
    ctext = xmlmap.NodeListField('rights:Context', Context)

    def add_ctext(self, new_ctext):
        self.create_holder()
        self.ctext.append(new_ctext)
        ctext_list = [str(ctx.id) for ctx in self.ctext]
        self.holder.context_ids = ' '.join(ctext_list)

def make_rights():
    m = Rights()
    h = Holder()
    m.holder=h
    return m
