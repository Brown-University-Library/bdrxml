# coding: utf-8
from __future__ import unicode_literals

#Default foxml from the reference exmample - http://fedora-commons.org/documentation/3.3.1/ - http://fedora-commons.org/documentation/3.3.1/attachments/4718716/4915209.xml
FOX = """
<foxml:digitalObject VERSION="1.1" PID="demo:999" xsi:schemaLocation="info:fedora/fedora-system:def/foxml# http://www.fedora.info/definitions/1/0/foxml1-1.xsd" xmlns:foxml="info:fedora/fedora-system:def/foxml#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <foxml:objectProperties>
    <foxml:property NAME="info:fedora/fedora-system:def/model#state" VALUE="A"/>
    <foxml:property NAME="info:fedora/fedora-system:def/model#label" VALUE="BDR Object"/>
  </foxml:objectProperties>
  <foxml:datastream ID="DC" STATE="A" CONTROL_GROUP="X">
    <foxml:datastreamVersion FORMAT_URI="http://www.openarchives.org/OAI/2.0/oai_dc/"
                             ID="DC.0" MIMETYPE="text/xml"
                             LABEL="Dublin Core Record for this object">
      <foxml:xmlContent>
        <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/">
        </oai_dc:dc>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
  <foxml:datastream ID="RELS-EXT" CONTROL_GROUP="X">
    <foxml:datastreamVersion FORMAT_URI="info:fedora/fedora-system:FedoraRELSExt-1.0"
                             ID="RELS-EXT.0" MIMETYPE="application/rdf+xml"
                             LABEL="RDF Statements about this object">
      <foxml:xmlContent>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                 xmlns:rel="info:fedora/fedora-system:def/relations-external#"
                 xmlns:myns="http://www.nsdl.org/ontologies/relationships#"
                 xmlns:dc="http://purl.org/dc/elements/1.1/"
                 xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/">
          <rdf:Description rdf:about="info:fedora/demo:999">
          </rdf:Description>
        </rdf:RDF>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
</foxml:digitalObject>
"""

from eulxml import xmlmap
from eulxml.xmlmap.dc import DublinCore
from eulxml.xmlmap import load_xmlobject_from_file
from eulxml.xmlmap  import load_xmlobject_from_string
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeField, NodeListField

#Local xml maps
from .mets import BDRMets, METS_NAMESPACE
from .rels import RelsExt, RelsInt
from .rights import Rights, RIGHTS_NAMESPACE
from .irMetadata import IR, IR_NAMESPACE


FOXNS = 'info:fedora/fedora-system:def/foxml#'
RDFNS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

class Common(xmlmap.XmlObject):
    """
    Base class for FOXML.
    """
    ROOT_NS = FOXNS
    ROOT_NAME = 'foxml'
    ROOT_NAMESPACES = {'foxml': FOXNS,
                       'rdf': RDFNS,
                       'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/'}
    SCHEMA = 'info:fedora/fedora-system:def/foxml#'

class DatastreamCommon(xmlmap.XmlObject):
    """
    Namespaces inherited elsewhere.
    """
    ROOT_NS = FOXNS
    ROOT_NAMESPACES = {'foxml': FOXNS}
    
class Content(Common):
    """
    Content of a datastream.
    """
    ROOT_NAME = 'xmlContent'
    #<foxml:contentLocation REF="http://icarus.lib.virginia.edu/images/iva/archerd05small.jpg" TYPE="URL"/>


class ContentLocation(DatastreamCommon):
    """
    For managed or externally reference datastreams.
    """
    ROOT = 'contentLocation'
    #This can be a reference to a local file if Fedora is configured to ingest from local paths
    #E.g. file:/tmp/photo.jpg
    href = SF('@REF')
    type = SF('@TYPE')
    
class DatastreamVersion(xmlmap.XmlObject):
    """
    Creates a version of a datastream.
    """
    ROOT_NS = FOXNS
    ROOT_NAME = 'datastreamVersion'
    ROOT_NAMESPACES = {'foxml': FOXNS}
    format = SF('@FORMAT_URI')
    id = SF('@ID')
    mimetype = SF('@MIMETYPE')
    label = SF('@LABEL')
    content = NodeField('foxml:xmlContent', Content)
    # content_list = NodeListField('foxml:xmlContent', Content)
    content_location = NodeField('foxml:contentLocation', ContentLocation)

class InlineRights(DatastreamVersion):
    """
    Handles inline METS like the BDR.  Only deference is adding the mets namespace.
    """
    #Handle mets slightly differently
    ROOT_NS = FOXNS
    ROOT_NAMESPACES = {'foxml': FOXNS,
                       'rights': RIGHTS_NAMESPACE}
    content = NodeField('foxml:xmlContent/rights:RightsDeclarationMD', Content)

class InlineIR(DatastreamVersion):
    """
    Handles inline METS like the BDR.  Only deference is adding the mets namespace.
    """
    #Handle mets slightly differently
    ROOT_NS = FOXNS
    ROOT_NAMESPACES = {'foxml': FOXNS,
                       'ir': IR_NAMESPACE}
    content = NodeField('foxml:xmlContent/ir:irData', Content)

class InlineMets(DatastreamVersion):
    """
    Handles inline METS like the BDR.  Only deference is adding the mets namespace.
    """
    #Handle mets slightly differently
    ROOT_NS = FOXNS
    ROOT_NAMESPACES = {'foxml': FOXNS,
                       'METS': METS_NAMESPACE}
    content = NodeField('foxml:xmlContent/METS:mets', Content)
    
class InlineRelsInt(DatastreamVersion):
    """
    Handles inline RELS-INT.  Difference from generic datastream is that it adds
    the RDF namespace. 
    """
    #Handle rels-int slightly differently
    ROOT_NS = FOXNS
    ROOT_NAMESPACES = {'foxml': FOXNS,
                       'rdf': RDFNS}
    content = NodeField('foxml:xmlContent/rdf:RDF', Content)
    content_list = NodeListField('foxml:xmlContent/rdf:RDF', Content)
    
class Datastream(xmlmap.XmlObject):
    """
    Basic properties and attributes for datastreams.
    """
    ROOT_NS = FOXNS
    ROOT_NAMESPACES = {'foxml': FOXNS}
    ROOT_NAME = 'datastream'
    id = SF('@ID')
    state = SF('@STATE')
    control_group = SF('@CONTROL_GROUP')
    versionable = SF('@VERSIONABLE')
    version =  NodeListField('datastreamVersion', DatastreamVersion)

class ObjectProperties(Common):
    """
    Foxml objectProperties
    """
    ROOT_NAME = 'property'
    value = SF('@VALUE')
    name = SF('@NAME')
    
class Fox(Common):
    ROOT_NAME = 'digitalObject'
    version = SF('@VERSION')
    pid = SF('@PID')
    object_properties = NodeListField('foxml:objectProperties/properties', ObjectProperties)
    datastream = NodeListField('foxml:datastream', Datastream)
    #Inclde DC and RELS-EXT since they required
    dc = NodeField('foxml:datastream[@ID="DC"]/foxml:datastreamVersion/foxml:xmlContent/oai_dc:dc', DublinCore)
    rels_ext = NodeField('foxml:datastream[@ID="RELS-EXT"]/foxml:datastreamVersion/foxml:xmlContent/rdf:RDF', RelsExt)

def make():
    #Create a basic BDR-ish FOXML document to get started. 
    doc = load_xmlobject_from_string(FOX, Fox)
    return doc
