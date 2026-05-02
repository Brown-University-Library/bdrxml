import os
import subprocess
import sys
import textwrap
import unittest

from bdrxml import schema_resolver


class SchemaResolverTest(unittest.TestCase):

    def test_schema_uri_maps_to_package_file(self):
        local_path = schema_resolver.schema_uri_or_path_to_local_path(
            'http://www.loc.gov/standards/mods/v3/mods-3-4.xsd')
        self.assertEqual(os.path.basename(local_path), 'mods-3-4.xsd')
        self.assertTrue(os.path.exists(local_path))

    def test_unknown_schema_uri_is_unchanged(self):
        uri = 'http://example.com/schema.xsd'
        self.assertEqual(schema_resolver.schema_uri_or_path_to_local_path(uri), uri)

    def test_darwincore_validation_helper_import_still_works(self):
        from bdrxml.darwincore import get_schema_validation_errors
        self.assertIs(get_schema_validation_errors,
                      schema_resolver.get_schema_validation_errors)

    def test_mods_import_uses_local_schema_for_eulxml_mods_34(self):
        script = textwrap.dedent('''
            import eulxml.xmlmap as xmlmap
            import eulxml.xmlmap.core as xmlmap_core

            original_loader = xmlmap_core.load_xmlobject_from_file

            def fail_on_http(filename, *args, **kwargs):
                if isinstance(filename, str) and filename.startswith(('http://', 'https://')):
                    raise RuntimeError('unexpected remote schema load: %s' % filename)
                return original_loader(filename, *args, **kwargs)

            xmlmap_core.load_xmlobject_from_file = fail_on_http
            xmlmap.load_xmlobject_from_file = fail_on_http

            from bdrxml import mods
            assert mods.Mods
        ''')
        subprocess.check_output([sys.executable, '-c', script],
                                cwd=os.getcwd(), stderr=subprocess.STDOUT)


def suite():
    suite = unittest.makeSuite(SchemaResolverTest, 'test')
    return suite


if __name__ == '__main__':
    unittest.main()
