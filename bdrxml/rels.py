# coding: utf-8
from __future__ import unicode_literals
from eulxml import xmlmap
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeListField
from eulxml.xmlmap import XmlObject


XMLNS = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'

class Common(XmlObject):
    ROOT_NS = XMLNS
    ROOT_NAME = 'RDF'
    ROOT_NAMESPACES = {
      'rdf': XMLNS,
      'fedora-model': 'info:fedora/fedora-system:def/model#',
      'rel': 'info:fedora/fedora-system:def/relations-external#'
      }
    

## rels-int classes ##

'''
Sample output...

<foxml:datastream xmlns:foxml="info:fedora/fedora-system:def/foxml#" ID="RELS-INT" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
  <foxml:datastreamVersion xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" ID="RELS-INT.0" LABEL="Internal Datastream Relationships" MIMETYPE="application/rdf+xml" FORMAT_URI="info:fedora/fedora-system:FedoraRELSInt-1.0">
    <foxml:xmlContent>
      <rdf:RDF>
        <rdf:Description xmlns:fedora-model="info:fedora/fedora-system:def/model#" rdf:about="info:fedora/test:123/TIFF">
          <fedora-model:downloadFilename>AB_123.tif</fedora-model:downloadFilename>
        </rdf:Description>
        <rdf:Description xmlns:fedora-model="info:fedora/fedora-system:def/model#" rdf:about="info:fedora/test:234/JP2">
          <fedora-model:downloadFilename>AB_123.jp2</fedora-model:downloadFilename>
        </rdf:Description>
      </rdf:RDF>
    </foxml:xmlContent>
  </foxml:datastreamVersion>
</foxml:datastream>
'''

class Description(Common):
  ROOT_NAME = 'Description'
  # about = SF('rdf:Description/@rdf:about')
  about = SF('@rdf:about')
  download_filename = SF( 'fedora-model:downloadFilename' )

class RelsInt(Common):
    descriptions = xmlmap.NodeListField( 'rdf:Description', Description )


## rels-ext classes ##

"""
Sample output...

<foxml:datastream ID="RELS-EXT" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
  <foxml:datastreamVersion ID="RELS-EXT.0" LABEL="RDF Statements about this object" CREATED="2012-03-09T14:11:58.990Z" MIMETYPE="application/rdf+xml" FORMAT_URI="info:fedora/fedora-system:FedoraRELSExt-1.0" SIZE="299">
    <foxml:xmlContent>
      <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:fedora-model="info:fedora/fedora-system:def/model#">
        <rdf:Description rdf:about="info:fedora/test:1000009025">
          <fedora-model:hasModel rdf:resource="info:fedora/bdr-cmodel:txt"/>
        </rdf:Description>
      </rdf:RDF>
    </foxml:xmlContent>
  </foxml:datastreamVersion>
</foxml:datastream>
"""

class Cmodel(Common):
    ROOT_NS = 'info:fedora/fedora-system:def/model#'
    ROOT_NAME = 'hasModel'
    name = SF('@rdf:resource')

    def __unicode__(self):
        return self.name
            
class MemberOf( Common ):
  ROOT_NS = 'info:fedora/fedora-system:def/relations-external#'
  ROOT_NAME = 'isMemberOf'
  name = SF( '@rdf:resource' )
  def __unicode__( self ):
    return self.name
       
class RelsExt(Common):
  about = SF('rdf:Description/@rdf:about')
  model = xmlmap.NodeListField('rdf:Description/fedora-model:hasModel', Cmodel)
  is_member_of = xmlmap.NodeListField( 'rdf:Description/rel:isMemberOf', MemberOf )
