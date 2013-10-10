import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.rights import (
    Rights, 
    make_rights,
    make_context,
    RightsBuilder,
)


class RightsReadWrite(unittest.TestCase):
    def setUp(self):
#basic right
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

EMPTY_RIGHTS_XML = """<rights:RightsDeclarationMD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rights="http://cosimo.stanford.edu/sdr/metsrights/" xsi:schemaLocation="http://cosimo.stanford.edu/sdr/rights http://cosimo.stanford.edu/sdr/metsrights.xsd"><rights:RightsHolder/></rights:RightsDeclarationMD>"""

RIGHTS_WITH_USERS = """<rights:RightsDeclarationMD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rights="http://cosimo.stanford.edu/sdr/metsrights/" xsi:schemaLocation="http://cosimo.stanford.edu/sdr/rights http://cosimo.stanford.edu/sdr/metsrights.xsd">
  <rights:RightsHolder CONTEXTIDS="rights000 rights001 rights002"/>
  <rights:Context CONTEXTID="rights000">
    <rights:Permissions DELETE="false" DISCOVER="true" DISPLAY="true" MODIFY="false"/>
    <rights:UserName USERTYPE="USER">johnny@brown.edu</rights:UserName>
  </rights:Context>
  <rights:Context CONTEXTID="rights001">
    <rights:Permissions DELETE="false" DISCOVER="false" DISPLAY="true" MODIFY="false"/>
    <rights:UserName USERTYPE="USER">jack@brown.edu</rights:UserName>
  </rights:Context>
  <rights:Context CONTEXTID="rights002">
    <rights:Permissions DELETE="false" DISCOVER="false" DISPLAY="false" MODIFY="true"/>
    <rights:UserName USERTYPE="USER">jim@brown.edu</rights:UserName>
  </rights:Context>
</rights:RightsDeclarationMD>
"""
class Builder(unittest.TestCase):
    """Test for the rights builder"""
    def setUp(self):
        self.builder = RightsBuilder()
    
    def test_basicBuild(self):
        """If nothing has been added to the builder then the builder should serialize to the same as EMPTY_RIGHTS_XML"""
        rights = self.builder.build()
        rights_str = rights.serialize()
        self.assertEqual(rights_str, EMPTY_RIGHTS_XML)

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

    def test_add_reader_and_build(self):
        self.builder.addReader('jack@brown.edu')
        self.builder.addReader('jack@brown.edu')
        self.builder.addEditor('jim@brown.edu')
        self.builder.addReader('johnny@brown.edu').addDiscoverer('johnny@brown.edu')
        rights = self.builder.build()
        rights_str = rights.serialize(pretty=True)
        self.assertEqual(rights_str, RIGHTS_WITH_USERS)


def suite():
    suite1 = unittest.makeSuite(RightsReadWrite, 'test')
    suite2 = unittest.makeSuite(Builder, 'test')
    alltests = unittest.TestSuite((suite1, suite2))
    return alltests

if __name__ == '__main__':
    unittest.main()
        
