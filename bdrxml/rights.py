# coding: utf-8
from __future__ import unicode_literals
from eulxml import xmlmap
from eulxml.xmlmap import XmlObject
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import StringListField as SFL
from eulxml.xmlmap import SimpleBooleanField as BF
from itertools import chain
RIGHTS_NAMESPACE = 'http://cosimo.stanford.edu/sdr/metsrights/'
XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'


class HydraRights(XmlObject):
    ROOT_NAMESPACES = {
               'hydra': 'http://hydra-collab.stanford.edu/schemas/rightsMetadata/v1',
    }
    ROOT_NAME = 'rightsMetadata'

    discover_access_group = SFL('hydra:access[@type="discover"]/hydra:machine/hydra:group')
    discover_access_person = SFL('hydra:access[@type="discover"]/hydra:machine/hydra:person')
    read_access_group = SFL('hydra:access[@type="read"]/hydra:machine/hydra:group')
    read_access_person = SFL('hydra:access[@type="read"]/hydra:machine/hydra:person')
    edit_access_group = SFL('hydra:access[@type="edit"]/hydra:machine/hydra:group')
    edit_access_person = SFL('hydra:access[@type="edit"]/hydra:machine/hydra:person')
    delete_access_group = SFL('hydra:access[@type="delete"]/hydra:machine/hydra:group')
    delete_access_person = SFL('hydra:access[@type="delete"]/hydra:machine/hydra:person')

    def index_data(self):
        return {
            'discover_access_group_ssim': sorted(self.discover_access_group),
            'discover_access_person_ssim': sorted(self.discover_access_person),
            'read_access_group_ssim': sorted(self.read_access_group),
            'read_access_person_ssim': sorted(self.read_access_person),
            'edit_access_group_ssim': sorted(self.edit_access_group),
            'edit_access_person_ssim': sorted(self.edit_access_person),
            'delete_access_group_ssim': sorted(self.delete_access_group),
            'delete_access_person_ssim': sorted(self.delete_access_person),
        }

    def index_data_bdr(self):
        return self.get_builder().build_bdr().index_data()

    def index_data_hydra(self):
        return self.index_data()

    def get_builder(self):
        """Creates a RightsBuilder based on the information stored in the this HydraRights object"""
        return RightsBuilder(
            discoverers = set(chain(self.discover_access_person, self.discover_access_group)),
            readers = set(chain(self.read_access_person, self.read_access_group)),
            editors = set(chain(self.edit_access_person, self.edit_access_group)),
            deleters = set(chain(self.delete_access_person, self.delete_access_group))
        )


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
    usertype = SF('rights:UserName/@USERTYPE')
    username = SF('rights:UserName')
    delete = BF('rights:Permissions/@DELETE','true','false')
    discover = BF('rights:Permissions/@DISCOVER','true','false')
    display = BF('rights:Permissions/@DISPLAY','true','false')
    modify = BF('rights:Permissions/@MODIFY','true','false')


def make_context():
    """Creates and empty context and explicitly assigns all permissions to false"""
    c = Context()
    c.delete = False
    c.discover = False
    c.display = False
    c.modify = False
    return c


class Holder(Common):
    ROOT_NAME = 'RightsHolder'
    context_ids = SF('@CONTEXTIDS')
    name = SF('rights:RightsHolderName')


class Rights(Common):
    ROOT_NAME = 'RightsDeclarationMD'
    XSD_SCHEMA = "http://cosimo.stanford.edu/sdr/rights http://cosimo.stanford.edu/sdr/metsrights.xsd"
    schema_location = SF('@xsi:schemaLocation', 'self')

    category = SF('@RIGHTSCATEGORY')
    holder = xmlmap.NodeField('rights:RightsHolder', Holder)
    #Can't call this context - it's a property inherited from the XMLMap
    ctext = xmlmap.NodeListField('rights:Context', Context)

    def add_ctext(self, new_ctext):
        self.create_holder()
        self.ctext.append(new_ctext)
        ctext_list = [str(ctx.id) for ctx in self.ctext]
        self.holder.context_ids = ' '.join(ctext_list)

    def get_ctext_for(self, user_name):
        return next((ctx for ctx in self.ctext if ctx.username == user_name))

    def index_data(self):
        return {
            'discover': sorted([ctx.username for ctx in self.ctext if ctx.discover]),
            'display': sorted([ctx.username for ctx in self.ctext if ctx.display]),
            'modify': sorted([ctx.username for ctx in self.ctext if ctx.modify]),
            'delete': sorted([ctx.username for ctx in self.ctext if ctx.delete]),
        }

    def get_builder(self):
        index = self.index_data()
        return RightsBuilder(
            discoverers = set(index['discover']),
            readers = set(index['display']),
            editors = set(index['modify']),
            deleters = set(index['delete'])
        )

    def index_data_bdr(self):
        return self.index_data()

    def index_data_hydra(self):
        return self.get_builder().build_hydra().index_data()


def make_rights():
    """Create a basic BDR rights object and instantiates a holder node."""
    m = Rights()
    m.create_holder()
    m.schema_location = Rights.XSD_SCHEMA
    return m


class RightsBuilder(object):
    """Base builder class for object rights.  Can build BDR Rights or Hydra Rights"""
    def __init__(self, discoverers=None, readers=None, editors=None, deleters=None, owners=None):
        super(RightsBuilder, self).__init__()
        self._discoverers = discoverers or set()
        self._readers = readers or set()
        self._editors = editors or set()
        self._deleters = deleters or set()
        self._owners = owners or set()
        for identity in self._owners:
            self.addOwner(identity)
    
    def addDiscoverer(self, identifier):
        self._discoverers.add(identifier)
        return self

    def addReader(self, identifier):
        self._readers.add(identifier)
        return self
        
    def addEditor(self, identifier):
        self._editors.add(identifier)
        return self

    def addDeleter(self, identifier):
        self._deleters.add(identifier)
        return self

    def addOwner(self, identifier):
        self.addDiscoverer(identifier)
        self.addReader(identifier)
        self.addEditor(identifier)
        self.addDeleter(identifier)
        return self
    
    @property
    def all_identities(self):
        return set(self._discoverers) | set(self._readers) | set(self._editors) | set(self._deleters) | set(self._owners)

    def __eq__(self, other):
        """Custom equality operator."""
        _NOTFOUND = object()
        for attr in ['_readers', '_editors', '_deleters', '_discoverers']:
            v1, v2 = [getattr(obj, attr, _NOTFOUND) for obj in [self, other]]
            if v1 is _NOTFOUND or v2 is _NOTFOUND:
                return False
            elif v1 != v2:
                return False
        return True

    def build(self):
        """Default Build.  Currently creates a BDR Rights object"""
        return self.build_bdr()

    def build_bdr(self):
        """Build a BDR Rights Object"""
        return BDRRightsBuilder(self).build()

    def build_hydra(self):
        """Build a Hydra compliant Rights object"""
        return HydraRightsBuilder(self).build()


class BDRRightsBuilder(object):

    def __init__(self, base_builder):
        super(BDRRightsBuilder, self).__init__()
        self.base_builder = base_builder
        
    def _identity_is_person(self, identity):
        return '@' in identity

    def _build_bdr_context(self, identity=None):
        user_type = "INDIVIDUAL" if self._identity_is_person(identity) else "GROUP"

        new_context = make_context()
        new_context.username = identity
        new_context.discover = identity in self.base_builder._discoverers | self.base_builder._owners
        new_context.display = identity in self.base_builder._readers | self.base_builder._owners
        new_context.modify = identity in self.base_builder._editors | self.base_builder._owners
        new_context.delete = identity in self.base_builder._deleters | self.base_builder._owners
        new_context.usertype = user_type
        return new_context

    def _build_contexts(self):
        return [self._build_bdr_context(identity) for identity in self.base_builder.all_identities]

    def build(self):
        rights = make_rights()
        for number, ctext in enumerate(self._build_contexts()):
            ctext.id = "rights%03d" % number
            rights.add_ctext(ctext)
        return rights
    

class HydraRightsBuilder(object):

    def __init__(self, base_builder):
        super(HydraRightsBuilder, self).__init__()
        self.base_builder = base_builder

    def _identity_is_person(self, identity):
        return '@' in identity
        
    def _partition_users_groups(self, identity_list):
        people = [ identity for identity in identity_list if self._identity_is_person(identity) ]
        groups = [ identity for identity in identity_list if not self._identity_is_person(identity) ]
        return groups, people

    def build(self):
        rights = HydraRights()

        groups, people = self._partition_users_groups(self.base_builder._readers | self.base_builder._owners)
        rights.read_access_group = groups
        rights.read_access_person = people

        groups, people = self._partition_users_groups(self.base_builder._editors | self.base_builder._owners)
        rights.edit_access_group = groups
        rights.edit_access_person = people

        groups, people = self._partition_users_groups(self.base_builder._discoverers | self.base_builder._owners)
        rights.discover_access_group = groups
        rights.discover_access_person = people

        groups, people = self._partition_users_groups(self.base_builder._deleters | self.base_builder._owners)
        rights.delete_access_group = groups
        rights.delete_access_person = people

        return rights
