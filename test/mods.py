import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.mods import Mods, make_mods, MODS_SCHEMA, LocalTopic

class ModsReadWrite(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.mods = make_mods()
        
    def test_round_trip(self):
        self.mods.title = "Sample title"
        self.mods.publisher = "BUL"
        mods_str = self.mods.serialize(pretty=False)
        loaded = load_xmlobject_from_string(mods_str, Mods)
        self.assertEqual(loaded.title, 'Sample title')
        self.assertEqual(loaded.publisher, 'BUL')
        #self.assertTrue(MODS_SCHEMA in loaded.schema_location)
        #self.mods.schema_location = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-0.xsd'
        #print self.mods.serialize(pretty=True)

    def test_subjects(self):
        self.mods.title = "Sample"
        local = ['sample', 'test']
        for keyword in local:
            subject = LocalTopic()
            subject.topic = keyword
            self.mods.local_topic.append(subject)
        new_mods = load_xmlobject_from_string(self.mods.serialize(), Mods)
        self.assertEqual(local, [n.topic for n in new_mods.local_topic])



def suite():
    suite = unittest.makeSuite(ModsReadWrite, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
