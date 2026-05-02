"""Package-local schema resolution helpers.

This module keeps bdrxml schema validation and selected import-time schema
lookups from depending on remote HTTP schema URLs. The immediate issue is
eulxml 1.1.3 loading MODS 3.4 from LOC while defining SchemaField-backed MODS
classes during import. bdrxml installs a narrow shim for known eulxml schema
URLs and leaves unknown paths/URLs untouched.
"""

import os

from lxml import etree


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(CURRENT_DIR, 'schemas')

SCHEMA_URI_MAP = {
    'http://www.loc.gov/standards/mods/v3/mods-3-4.xsd': 'mods-3-4.xsd',
    # If eulxml ever loads MODS_SCHEMA directly, map its mods.xsd URL here.
}


def schema_path(schema_name):
    return os.path.join(SCHEMA_DIR, schema_name)


def schema_uri_or_path_to_local_path(value):
    schema_name = SCHEMA_URI_MAP.get(value)
    if schema_name:
        return schema_path(schema_name)
    return value


def get_schema_validation_errors(schema_name, lxml_node):
    with open(schema_path(schema_name), 'rb') as f:
        xmlschema = etree.XMLSchema(etree.parse(f))
        if xmlschema.validate(lxml_node):
            return []
        else:
            return xmlschema.error_log


def install_eulxml_schema_resolver():
    """Resolve selected eulxml schema URLs from bdrxml's bundled schemas."""
    import eulxml.xmlmap as xmlmap
    import eulxml.xmlmap.core as xmlmap_core

    current_loader = xmlmap_core.load_xmlobject_from_file
    if getattr(current_loader, '_bdrxml_schema_resolver', False):
        return

    def load_xmlobject_from_file(filename, xmlclass=xmlmap_core.XmlObject,
            validate=False, resolver=None):
        local_filename = schema_uri_or_path_to_local_path(filename)
        return current_loader(local_filename, xmlclass=xmlclass,
                              validate=validate, resolver=resolver)

    load_xmlobject_from_file._bdrxml_schema_resolver = True
    load_xmlobject_from_file._bdrxml_original_loader = current_loader

    xmlmap_core.load_xmlobject_from_file = load_xmlobject_from_file
    xmlmap.load_xmlobject_from_file = load_xmlobject_from_file
