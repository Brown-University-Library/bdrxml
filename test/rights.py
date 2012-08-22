import os
import unittest
from lxml import etree
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.rights import Rights, make_rights, Context, Holder, RIGHTS_NAMESPACE


class RightsReadWrite(unittest.TestCase):
    def setUp(self):
#basic right
        self.rights = make_rights()

    def init_holder(self):
        #holder = Holder()
        #holder.name="Johnny"
        #holder.context_ids="rights1"
        #self.rights.holder=holder
        self.rights.holder.name="Johnny"
    
    def init_context(self, ctx_name):
        context = Context()
        context.cclass = "REPOSITORY MGR"
        context.usertype = "GROUP"
        context.id = ctx_name
        context.delete = 'y'
        context.discover = 'true' 
        context.display = 'true' 
        context.modify = 'true' 
        self.rights.add_ctext(context)
    
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


def suite():
    suite = unittest.makeSuite(RightsReadWrite, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
        
