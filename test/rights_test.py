# coding: utf-8
from __future__ import unicode_literals
import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.rights import (
    Rights, 
    HydraRights,
    make_rights,
    make_context,
    RightsBuilder,
)

class HydraRightsReadWrite(unittest.TestCase):
    FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<rightsMetadata xmlns="http://hydra-collab.stanford.edu/schemas/rightsMetadata/v1" version="0.1">
    <access type="discover">
        <machine>
            <group>group2</group>
        </machine>
    </access>
    <access type="read">
        <machine>
            <group>group3</group>
            <group>group9</group>
            <group>group8</group>
            <person>user3</person>
        </machine>
    </access>
    <access type="edit">
        <machine>
            <person>bob1</person>
            <person>sally2</person>
        </machine>
    </access>
</rightsMetadata>"""

    def setUp(self):
        self.rights = load_xmlobject_from_string(self.FIXTURE.encode('utf8'), HydraRights)

    def test_group_access(self):
        self.assertEqual( ['group3', 'group9', 'group8'], self.rights.read_access_group )
        
    def test_person_access(self):
        self.assertEqual( ['bob1', 'sally2'], self.rights.edit_access_person )
    
    #Additional testing on reading and assigning to string lists covered in eulxml
    
    def test_index_data(self):
        self.assertEqual({
            'read_access_group_ssim': sorted(['group3', 'group9', 'group8']),
            'read_access_person_ssim': sorted(['user3',]),
            'edit_access_group_ssim': sorted([]),
            'edit_access_person_ssim': sorted(['bob1','sally2']),
            'discover_access_group_ssim': sorted(['group2']),
            'discover_access_person_ssim': sorted([]),
            'delete_access_group_ssim': sorted([]),
            'delete_access_person_ssim': sorted([]),
        }, self.rights.index_data())

    def test_index_data_bdr(self):
        self.assertEqual({
            'discover': sorted(['group2']),
            'display': sorted(['group3', 'group8', 'group9','user3', ]),
            'modify': sorted(['bob1','sally2']),
            'delete': sorted([]),
        }, self.rights.index_data_bdr())


class RightsReadWrite(unittest.TestCase):

    def setUp(self):
        self.rights = make_rights()

    def init_holder(self):
        self.rights.holder.name="Johnny"
    
    def init_context(self, ctx_name, username="johnny@brown.edu"):
        my_context = make_context()
        my_context.cclass = "REPOSITORY MGR"
        my_context.usertype = "GROUP"
        my_context.username =username
        my_context.id = ctx_name
        my_context.delete = 'y'
        my_context.modify = 'true' 
        self.rights.add_ctext(my_context)
    
    def test_holder(self):
        self.init_holder()
        rights_str = self.rights.serialize(pretty=True)
        loaded = load_xmlobject_from_string(rights_str, Rights)
        self.assertEqual(loaded.holder.name, 'Johnny')
        #self.assertEqual(loaded.holder.context_ids, 'rights1')

    def test_contextNumber(self):
        self.init_context("rights1")
        rights_str = self.rights.serialize(pretty=True)
        loaded = load_xmlobject_from_string(rights_str, Rights)
        self.assertEqual(len(loaded.ctext), 1)

    def test_contextClass(self):
        self.init_context("rights1")
        rights_str = self.rights.serialize(pretty=True)
        loaded = load_xmlobject_from_string(rights_str, Rights)
        self.assertEqual(loaded.ctext[0].cclass, "REPOSITORY MGR")

    def test_multiContextAndHolder(self):
        self.init_context("rights1")
        self.init_context("rights2")
        self.init_context("rights3")
        self.init_holder()
        rights_str = self.rights.serialize(pretty=True)
        loaded = load_xmlobject_from_string(rights_str, Rights)
        self.assertEqual(len(loaded.ctext), 3)
        self.assertEqual(loaded.holder.context_ids, 'rights1 rights2 rights3')

    def test_get_context_exception(self):
        self.init_context("rights1")
        self.init_holder()
        self.assertRaises(StopIteration, self.rights.get_ctext_for, "BOB")

    def test_get_context(self):
        self.init_context("rights1", 'jack@brown.edu')
        self.init_context("rights2", 'jim@brown.edu')
        self.init_context("rights3", 'johnny@brown.edu')
        self.init_holder()
        tmp_ctext = self.rights.get_ctext_for("johnny@brown.edu")
        self.assertEqual(tmp_ctext.id, "rights3")

    def test_update_context(self):
        self.init_context("rights1", 'jack@brown.edu')
        self.assertEqual(self.rights.ctext[0].delete, True)
        ctx = self.rights.get_ctext_for('jack@brown.edu')
        setattr(ctx, 'delete', False)
        self.assertEqual(self.rights.ctext[0].delete, False)
    
    def test_index_data(self):
        self.init_context("rights1", 'jack@brown.edu')
        self.init_context("rights2", 'jim@brown.edu')
        self.init_context("rights3", 'johnny@brown.edu')
        self.assertEqual( {
            'discover': [],
            'display': [],
            'modify': [ 'jack@brown.edu', 'jim@brown.edu', 'johnny@brown.edu'],
            'delete': [ 'jack@brown.edu', 'jim@brown.edu', 'johnny@brown.edu'],
            },self.rights.index_data())

    def test_index_data_hydra(self):
        self.init_context("rights1", 'jack@brown.edu')
        self.init_context("rights2", 'jim@brown.edu')
        self.init_context("rights3", 'johnny@brown.edu')
        self.init_context("rights4", 'BROWN:GROUP')
        self.assertEqual({
            'read_access_group_ssim': sorted([]),
            'read_access_person_ssim': sorted([]),
            'edit_access_group_ssim': sorted(['BROWN:GROUP',]),
            'edit_access_person_ssim': sorted([ 'jack@brown.edu', 'jim@brown.edu', 'johnny@brown.edu']),
            'discover_access_group_ssim': sorted([]),
            'discover_access_person_ssim': sorted([]),
            'delete_access_group_ssim': sorted(['BROWN:GROUP']),
            'delete_access_person_ssim': sorted([ 'jack@brown.edu', 'jim@brown.edu', 'johnny@brown.edu',]),
        }, self.rights.index_data_hydra())


#remove the first line with the namespaces, because their order changes randomly
JOHNNY_RIGHTS = """
    <rights:Permissions DELETE="false" DISCOVER="true" DISPLAY="true" MODIFY="false"/>
    <rights:UserName USERTYPE="INDIVIDUAL">johnny@brown.edu</rights:UserName>
  </rights:Context>
"""
BROWN_GROUP_RIGHTS = """
    <rights:Permissions DELETE="false" DISCOVER="false" DISPLAY="true" MODIFY="false"/>
    <rights:UserName USERTYPE="GROUP">BROWN:GROUP</rights:UserName>
  </rights:Context>
"""
JACK_RIGHTS = """
    <rights:Permissions DELETE="false" DISCOVER="false" DISPLAY="true" MODIFY="false"/>
    <rights:UserName USERTYPE="INDIVIDUAL">jack@brown.edu</rights:UserName>
  </rights:Context>
"""
JIM_RIGHTS = """
    <rights:Permissions DELETE="false" DISCOVER="false" DISPLAY="false" MODIFY="true"/>
    <rights:UserName USERTYPE="INDIVIDUAL">jim@brown.edu</rights:UserName>
  </rights:Context>
"""
HYDRA_RIGHTS_WITH_USERS = """<rightsMetadata xmlns:hydra="http://hydra-collab.stanford.edu/schemas/rightsMetadata/v1">
  <hydra:access type="read">
    <hydra:machine>
      <hydra:group>BROWN:GROUP</hydra:group>
      <hydra:person>johnny@brown.edu</hydra:person>
      <hydra:person>jack@brown.edu</hydra:person>
    </hydra:machine>
  </hydra:access>
  <hydra:access type="edit">
    <hydra:machine>
      <hydra:person>jim@brown.edu</hydra:person>
    </hydra:machine>
  </hydra:access>
  <hydra:access type="discover">
    <hydra:machine>
      <hydra:person>johnny@brown.edu</hydra:person>
    </hydra:machine>
  </hydra:access>
</rightsMetadata>
"""

class Builder(unittest.TestCase):

    def setUp(self):
        self.builder = RightsBuilder()
    
    def test_empty(self):
        """If no identities have been added then the result of all_identities should be an empty set"""
        self.assertEqual(set([]), self.builder.all_identities)
        
    def test_addowner(self):
        """If we add one owner then they should have access to all privleges"""
        self.builder.addOwner('johnny')
        rights = self.builder.build()
        ctext = rights.ctext[0]
        self.assertTrue(ctext.display)
        self.assertTrue(ctext.discover)
        self.assertTrue(ctext.modify)
        self.assertTrue(ctext.delete)

    def test_addreader(self):
        """If we add one reader then they should be the only identiry in the set of all_identities"""
        self.builder.addReader('johnny')
        self.assertEqual(set(['johnny']), self.builder.all_identities)

    def test_add_users_and_build(self):
        self.builder.addReader('jack@brown.edu').addReader('BROWN:GROUP')
        self.builder.addReader('jack@brown.edu')
        self.builder.addReader('jack@brown.edu')
        self.builder.addEditor('jim@brown.edu')
        self.builder.addReader('johnny@brown.edu').addDiscoverer('johnny@brown.edu')
        rights = self.builder.build()
        rights_str = rights.serialize(pretty=True)
        self.assertTrue(JACK_RIGHTS.encode('utf8') in rights_str)
        self.assertTrue(JOHNNY_RIGHTS.encode('utf8') in rights_str)
        self.assertTrue(JIM_RIGHTS.encode('utf8') in rights_str)
        self.assertTrue(BROWN_GROUP_RIGHTS.encode('utf8') in rights_str)
        
    def test_add_users_and_build_hydra(self):
        self.builder.addReader('jack@brown.edu').addReader('BROWN:GROUP')
        self.builder.addReader('jack@brown.edu')
        self.builder.addEditor('jim@brown.edu')
        self.builder.addReader('johnny@brown.edu').addDiscoverer('johnny@brown.edu')
        rights = self.builder.build_hydra()
        rights_str = rights.serialize(pretty=True)
        hydra_rights = load_xmlobject_from_string(rights_str, HydraRights)
        self.assertEqual(hydra_rights.discover_access_group, [])
        self.assertEqual(hydra_rights.discover_access_person, ['johnny@brown.edu'])
        self.assertEqual(hydra_rights.read_access_group, ['BROWN:GROUP'])
        self.assertEqual(sorted(hydra_rights.read_access_person), ['jack@brown.edu', 'johnny@brown.edu'])
        self.assertEqual(hydra_rights.edit_access_group, [])
        self.assertEqual(hydra_rights.edit_access_person, ['jim@brown.edu'])
        self.assertEqual(hydra_rights.delete_access_group, [])
        self.assertEqual(hydra_rights.delete_access_person, [])

    def test_getting_builder_back_from_bdr_rights(self):
        self.builder.addReader('jack@brown.edu').addReader('BROWN:GROUP')
        self.builder.addReader('jack@brown.edu')
        self.builder.addEditor('jim@brown.edu')
        self.builder.addReader('johnny@brown.edu').addDiscoverer('johnny@brown.edu')
        rights = self.builder.build()
        new_builder = rights.get_builder()
        self.assertEqual(new_builder, self.builder)

    def test_getting_builder_back_from_hydra_rights(self):
        self.builder.addReader('jack@brown.edu').addReader('BROWN:GROUP')
        self.builder.addReader('jack@brown.edu')
        self.builder.addEditor('jim@brown.edu')
        self.builder.addReader('johnny@brown.edu').addDiscoverer('johnny@brown.edu')
        rights = self.builder.build_hydra()
        new_builder = rights.get_builder()
        self.assertEqual(new_builder, self.builder)


def suite():
    suite1 = unittest.makeSuite(RightsReadWrite, 'test')
    suite2 = unittest.makeSuite(Builder, 'test')
    suite3 = unittest.makeSuite(HydraRightsReadWrite, 'test')
    alltests = unittest.TestSuite((suite1, suite2, suite3))
    return alltests

if __name__ == '__main__':
    unittest.main()
