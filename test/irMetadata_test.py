import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.irMetadata import IR, make_ir

class IRReadWrite(unittest.TestCase):
    def setUp(self):
        self.ir = make_ir()

    def test_WriteRead(self):
        self.ir.depositor_name = "Johnny"
        self.ir.depositor_email = "johnny@brown.edu"
        self.ir.date = "2012-05-31"
        self.ir.filename = "Multiple files"
        self.ir.collections_date = "2012-05-31"
        self.ir.collection = '598'

        ir_str = self.ir.serializeDocument(pretty=True)
        loaded = load_xmlobject_from_string(ir_str, IR)
        self.assertEqual(loaded.collection, '598')
        
    def test_MultiCollection(self):
        self.ir.depositor_name = "Johnny"
        self.ir.depositor_email = "johnny@brown.edu"
        self.ir.date = "2012-05-31"
        self.ir.filename = "Multiple files"
        self.ir.collections_date = "2012-05-31"
        self.ir.collection_list = ['598', '618']

        ir_str = self.ir.serializeDocument(pretty=True)
        loaded = load_xmlobject_from_string(ir_str, IR)
        self.assertEqual(loaded.collection_list, ['598', '618'])

def suite():
    suite = unittest.makeSuite(IRReadWrite, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()
