# coding: utf-8
from __future__ import unicode_literals
from eulxml import xmlmap
from eulxml.xmlmap import XmlObject
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import StringListField as SLF

IR_NAMESPACE = 'http://dl.lib.brown.edu/md/irdata'
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'

class IR(XmlObject):
    ROOT_NAMESPACES = {
               'ir': IR_NAMESPACE,
               'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
               }
    ROOT_NS = IR_NAMESPACE
    ROOT_NAME = 'irData'
    XSD_SCHEMA = "http://dl.lib.brown.edu/md/irdata http://dl.lib.brown.edu/md/irdata/ir.xsd"
    schema_location = SF('@xsi:schemaLocation', 'self')
    #xmlschema = xmlmap.loadSchema(XSD_SCHEMA)


    #Fields
    depositor_name = SF('ir:deposit/ir:depositor/ir:name')
    depositor_email = SF('ir:deposit/ir:depositor/ir:email')
    depositor_eppn = SF('ir:deposit/ir:depositor/ir:eppn')
    date = SF('ir:deposit/ir:date')
    filename = SF('ir:deposit/ir:filename')
    collections_date = SF('ir:collections/ir:date')
    collection = SF('ir:collections/ir:collection', required="False")
    collection_list = SLF('ir:collections/ir:collection',
                            verbose_name="Collections")

def make_ir():
    m = IR()
    m.schema_location = IR.XSD_SCHEMA
    return m
