import os
import unittest

from neuxml.xmlmap import load_xmlobject_from_file, load_xmlobject_from_string

from bdrxml.darwincore import make_simple_darwin_record_set
from bdrxml.mets import BDRMets, File, FileGrp, StructMap, make_mets
from bdrxml.mods import make_mods

BASE = os.path.dirname(os.path.abspath(__file__))

class MetsReadWrite(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.mets = load_xmlobject_from_file(os.path.join(BASE, 'data/cdi_mets.xml'),
                                             BDRMets)
        
    def test_read(self):
        #print self.mets.serialize(pretty=True)
        assert self.mets.rights is not None
        assert self.mets.rights.holder is not None
        self.assertEqual(self.mets.rights.holder.name, "Brown University")
        assert self.mets.mods is not None
        self.assertEqual(self.mets.mods.title, "Camp Grant Massacre")
        
    def test_create(self):
        mets = make_mets()
        #mods
        mods_section = make_mods()
        mods_section.title = 'sample'
        mets.create_mods()
        mets.mods = mods_section
        #dwc
        dwc_section = make_simple_darwin_record_set()
        dwc_section.create_simple_darwin_record()
        assert dwc_section.simple_darwin_record is not None
        dwc_section.simple_darwin_record.catalog_number = 'catalog number'
        mets.create_dwc()
        mets.dwc = dwc_section
        #ir
        mets.create_ir()
        assert mets.ir is not None
        mets.ir.filename = 'sample.txt'
        #filesec -> filegrp
        mets.create_filesec()
        fg = FileGrp()
        fg.id = u'GID1'
        fg.use = u'image-tiff'
        fi = File()
        fi.admid = u'TMD1'
        fi.groupid = u'GRP1'
        fi.id = u'FID1'
        fi.mimetype = u'image/tiff'
        fi.loctype = u'URL'
        fi.href = u'/the/path.tif'
        fg.file.append( fi )
        assert mets.filesec is not None
        mets.filesec.filegrp.append( fg )
        #structMap
        mets.create_structmap()  # not used but required for valid mets
        #serialize
        created_string = mets.serialize( pretty=True )
        #load
        loaded = load_xmlobject_from_string(created_string, BDRMets)
        #test
        assert loaded.mods is not None
        self.assertEqual(loaded.mods.title, 'sample')
        assert loaded.dwc is not None
        assert loaded.dwc.simple_darwin_record is not None
        self.assertEqual(loaded.dwc.simple_darwin_record.catalog_number, 'catalog number')
        assert loaded.ir is not None
        self.assertEqual(loaded.ir.filename, 'sample.txt')
        self.assertEqual( type(loaded.structmap), StructMap )
        assert loaded.filesec is not None
        self.assertEqual( loaded.filesec.filegrp[0].file[0].node.items(), [('ADMID', 'TMD1'), ('GROUPID', 'GRP1'), ('ID', 'FID1'), ('MIMETYPE', 'image/tiff')] )
        
        #TO DO - finish.  Also test helper called by studio.


def suite():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MetsReadWrite)
    return suite

if __name__ == '__main__':
    unittest.main()
