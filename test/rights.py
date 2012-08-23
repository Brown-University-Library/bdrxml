import os
import unittest
from lxml import etree
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.rights import Rights, make_rights, Context, make_context, Holder, RIGHTS_NAMESPACE


class RightsReadWrite(unittest.TestCase):
    def setUp(self):
#basic right
        self.rights = make_rights()

    def init_holder(self):
        self.rights.holder.name="Johnny"
    
    def init_context(self, ctx_name):
        my_context = make_context()
        my_context.cclass = "REPOSITORY MGR"
        my_context.usertype = "GROUP"
        my_context.username = "johnny@brown.edu"
        my_context.id = ctx_name
        my_context.delete = 'y'
        #my_context.discover = 'true' 
        #my_context.display = 'true' 
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
        print rights_str
        loaded = load_xmlobject_from_string(rights_str, Rights)
        self.assertEqual(len(loaded.ctext), 3)
        self.assertEqual(loaded.holder.context_ids, 'rights1 rights2 rights3')


def suite():
    suite = unittest.makeSuite(RightsReadWrite, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
        
