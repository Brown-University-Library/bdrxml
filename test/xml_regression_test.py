"""Checks shared XML behavior during the bdrxml 2.0 migration."""

import unittest

from lxml import etree

from bdrxml import darwincore, foxml, irMetadata, mets, mods, rels, rights


class ModsXmlRegressionTests(unittest.TestCase):
    def test_equivalent_fast_topic_keeps_one_subject_and_original_uri(self) -> None:
        """
        Checks equivalent FAST identifiers reuse a subject without altering its stored URI.
        """
        record = mods.make_mods()
        original_uri = 'http://id.worldcat.org/fast/00902025/'
        mods.add_topic(record, 'Architecture', label='Subjects', fast_uri=original_uri)
        mods.add_topic(record, 'Maps')
        mods.add_topic(record, 'Architecture', label='Subjects', fast_uri='http://id.worldcat.org/fast/902025')

        loaded = mods.Mods(node=etree.fromstring(record.serialize()))
        self.assertEqual([subject.topic for subject in loaded.subjects], ['Architecture', 'Maps'])
        subject = loaded.subjects[0]
        self.assertEqual(
            (subject.label, subject.authority, subject.authority_uri, subject.value_uri),
            ('Subjects', 'fast', 'http://id.worldcat.org/fast', original_uri),
        )

    def test_conflicting_topic_does_not_change_existing_xml(self) -> None:
        """
        Checks conflicting labels or identifiers fail without changing any stored metadata.
        """
        conflicts = [
            ('Other label', 'http://id.worldcat.org/fast/902025'),
            ('Subjects', 'http://id.worldcat.org/fast/902026'),
        ]
        for label, uri in conflicts:
            with self.subTest(label=label, uri=uri):
                record = mods.make_mods()
                mods.add_topic(record, 'Architecture', label='Subjects', fast_uri='http://id.worldcat.org/fast/902025')
                mods.add_topic(record, 'Maps')
                original = record.serialize()
                with self.assertRaisesRegex(Exception, 'mods object already has topic "Architecture"'):
                    mods.add_topic(record, 'Architecture', label=label, fast_uri=uri)
                self.assertEqual(record.serialize(), original)

    def test_replacing_names_and_clearing_genres_preserves_other_metadata(self) -> None:
        """
        Checks list edits remove old values while preserving titles and unmapped XML extensions.
        """
        record = mods.Mods(
            node=etree.fromstring(b"""
            <mods xmlns="http://www.loc.gov/mods/v3" xmlns:custom="urn:example:metadata">
              <titleInfo><title>Original title</title></titleInfo>
              <name><namePart>First author</namePart></name>
              <name><namePart>Second author</namePart></name>
              <genre>Old genre</genre><genre>Another old genre</genre>
              <extension><custom:note code="retain">Keep this annotation</custom:note></extension>
            </mods>
        """)
        )
        record.names = [
            mods.Name(
                type='personal',
                name_parts=[mods.NamePart(text='Céline & collaborators')],
                roles=[mods.Role(text='editor', authority='marcrelator')],
            )
        ]
        record.genres = []

        loaded = mods.Mods(node=etree.fromstring(record.serialize()))
        self.assertEqual(loaded.title, 'Original title')
        self.assertEqual(len(loaded.names), 1)
        self.assertEqual(loaded.names[0].name_parts[0].text, 'Céline & collaborators')
        self.assertEqual(loaded.names[0].type, 'personal')
        self.assertEqual([(role.text, role.authority) for role in loaded.names[0].roles], [('editor', 'marcrelator')])
        self.assertEqual(len(loaded.genres), 0)
        extension = loaded.node.find('{http://www.loc.gov/mods/v3}extension/{urn:example:metadata}note')
        assert extension is not None
        self.assertEqual((extension.text, extension.get('code')), ('Keep this annotation', 'retain'))


class RightsXmlRegressionTests(unittest.TestCase):
    def test_new_context_denies_permissions_and_creates_holder(self) -> None:
        """
        Checks adding a default context creates its holder reference and grants no permissions.
        """
        record = rights.Rights()
        context = rights.make_context()
        context.id = 'rights001'
        context.username = 'viewer@example.org'
        context.usertype = 'INDIVIDUAL'
        record.add_ctext(context)

        loaded = rights.Rights(node=etree.fromstring(record.serialize()))
        assert loaded.holder is not None
        self.assertEqual(loaded.holder.context_ids, 'rights001')
        self.assertEqual(len(loaded.ctext), 1)
        stored = loaded.get_ctext_for('viewer@example.org')
        self.assertEqual((stored.discover, stored.display, stored.modify, stored.delete), (False, False, False, False))
        permissions = stored.node.find('{http://cosimo.stanford.edu/sdr/metsrights/}Permissions')
        assert permissions is not None
        self.assertEqual(
            dict(permissions.attrib), {'DISCOVER': 'false', 'DISPLAY': 'false', 'MODIFY': 'false', 'DELETE': 'false'}
        )
        self.assertEqual(loaded.index_data(), {'discover': [], 'display': [], 'modify': [], 'delete': []})

    def test_mixed_permissions_survive_bdr_and_hydra_conversion(self) -> None:
        """
        Checks owners, people, and groups retain exactly their assigned permissions after conversion.
        """
        builder = rights.RightsBuilder(
            owners={'owner@example.org', 'curators'},
            discoverers={'catalogue'},
            readers={'reader@example.org', 'viewers'},
            editors={'editors'},
            deleters={'deleter@example.org'},
        )
        builder.addReader('reader@example.org')
        record = builder.build_bdr()
        loaded = rights.Rights(node=etree.fromstring(record.serialize()))
        expected_permissions = {
            'owner@example.org': (True, True, True, True),
            'curators': (True, True, True, True),
            'catalogue': (True, False, False, False),
            'reader@example.org': (False, True, False, False),
            'viewers': (False, True, False, False),
            'editors': (False, False, True, False),
            'deleter@example.org': (False, False, False, True),
        }
        self.assertEqual(len(loaded.ctext), len(expected_permissions))
        self.assertEqual(
            {ctx.username: (ctx.discover, ctx.display, ctx.modify, ctx.delete) for ctx in loaded.ctext},
            expected_permissions,
        )
        ids = [ctx.id for ctx in loaded.ctext]
        self.assertEqual(len(set(ids)), len(ids))
        assert loaded.holder is not None
        assert loaded.holder.context_ids is not None
        self.assertEqual(loaded.holder.context_ids.split(), ids)

        hydra = loaded.get_builder().build_hydra()
        restored = rights.HydraRights(node=etree.fromstring(hydra.serialize()))
        self.assertEqual(sorted(restored.read_access_group), ['curators', 'viewers'])
        self.assertEqual(sorted(restored.read_access_person), ['owner@example.org', 'reader@example.org'])
        self.assertEqual(sorted(restored.delete_access_group), ['curators'])
        self.assertEqual(sorted(restored.delete_access_person), ['deleter@example.org', 'owner@example.org'])
        converted = restored.get_builder().build_bdr()
        final = rights.Rights(node=etree.fromstring(converted.serialize()))
        self.assertEqual(
            {ctx.username: (ctx.discover, ctx.display, ctx.modify, ctx.delete) for ctx in final.ctext},
            expected_permissions,
        )


class ContainerXmlRegressionTests(unittest.TestCase):
    def test_ir_collection_edits_preserve_deposit_details(self) -> None:
        """
        Checks collection removal and addition preserve all deposit fields and escaped text.
        """
        record = irMetadata.make_ir()
        record.depositor_name = 'Renée & collaborators'
        record.depositor_email = 'depositor@example.org'
        record.depositor_eppn = 'account@example.org'
        record.date = '2020-02-03'
        record.filename = 'Plans & <notes>.xml'
        record.collections_date = '2020-02-04'
        record.collection_list = ['remove', 'retain']
        edited = irMetadata.IR(node=etree.fromstring(record.serialize()))
        del edited.collection_list[0]
        edited.collection_list.append('added')

        loaded = irMetadata.IR(node=etree.fromstring(edited.serialize()))
        self.assertEqual(list(loaded.collection_list), ['retain', 'added'])
        self.assertEqual(
            (
                loaded.depositor_name,
                loaded.depositor_email,
                loaded.depositor_eppn,
                loaded.date,
                loaded.filename,
                loaded.collections_date,
            ),
            (
                'Renée & collaborators',
                'depositor@example.org',
                'account@example.org',
                '2020-02-03',
                'Plans & <notes>.xml',
                '2020-02-04',
            ),
        )
        self.assertEqual(loaded.schema_location, record.schema_location)

    def test_mets_file_edits_preserve_other_groups_and_metadata(self) -> None:
        """
        Checks nested file edits preserve sibling groups, namespaced links, and descriptive metadata.
        """
        record = mets.make_mets()
        record.pid = 'example:42'
        record.mods = mods.make_mods()
        assert record.mods is not None
        record.mods.title = 'Collection title'
        record.rights = rights.RightsBuilder(readers={'viewers'}).build_bdr()
        record.filesec = mets.FileSec(
            filegrp=[
                mets.FileGrp(
                    id='master',
                    use='original',
                    file=[
                        mets.File(
                            id='first', mimetype='image/tiff', seq='1', loctype='URL', href='https://example.org/first.tif'
                        ),
                        mets.File(
                            id='second', mimetype='image/tiff', seq='2', loctype='URL', href='https://example.org/second.tif'
                        ),
                    ],
                ),
                mets.FileGrp(
                    id='preview',
                    use='thumbnail',
                    file=[
                        mets.File(id='thumb', mimetype='image/jpeg', loctype='URL', href='https://example.org/thumb.jpg'),
                    ],
                ),
            ]
        )
        edited = mets.BDRMets(node=etree.fromstring(record.serialize()))
        assert edited.filesec is not None
        edited.filesec.filegrp[0].file[0].href = 'https://example.org/revised.tif?a=1&b=2'
        del edited.filesec.filegrp[0].file[1]

        loaded = mets.BDRMets(node=etree.fromstring(edited.serialize()))
        assert loaded.filesec is not None
        self.assertEqual(
            [(group.id, group.use) for group in loaded.filesec.filegrp], [('master', 'original'), ('preview', 'thumbnail')]
        )
        self.assertEqual([len(group.file) for group in loaded.filesec.filegrp], [1, 1])
        first = loaded.filesec.filegrp[0].file[0]
        self.assertEqual((first.id, first.mimetype, first.seq, first.loctype), ('first', 'image/tiff', '1', 'URL'))
        self.assertEqual(first.href, 'https://example.org/revised.tif?a=1&b=2')
        self.assertEqual(loaded.filesec.filegrp[1].file[0].href, 'https://example.org/thumb.jpg')
        location = first.node.find('{http://www.loc.gov/METS/}FLocat')
        assert location is not None
        self.assertEqual(location.get('{http://www.w3.org/1999/xlink}href'), first.href)
        self.assertEqual(loaded.pid, 'example:42')
        assert loaded.mods is not None
        self.assertEqual(loaded.mods.title, 'Collection title')
        assert loaded.rights is not None
        self.assertEqual(loaded.rights.index_data(), {'discover': [], 'display': ['viewers'], 'modify': [], 'delete': []})

    def test_foxml_metadata_edits_do_not_leak_into_other_documents(self) -> None:
        """
        Checks Dublin Core and relationships survive serialization without changing another document.
        """
        first = foxml.make()
        second = foxml.make()
        unchanged = second.serialize()
        first.pid = 'example:42'
        assert first.dc is not None
        first.dc.title = 'Café & <plans>'
        first.dc.creator_list = ['First creator', 'Second creator']
        first.rels_ext = rels.RelsExt(
            about='info:fedora/example:42', is_member_of=[rels.MemberOf(name='info:fedora/example:collection')]
        )

        loaded = foxml.Fox(node=etree.fromstring(first.serialize()))
        self.assertEqual(loaded.pid, 'example:42')
        assert loaded.dc is not None
        self.assertEqual(loaded.dc.title, 'Café & <plans>')
        self.assertEqual(list(loaded.dc.creator_list), ['First creator', 'Second creator'])
        assert loaded.rels_ext is not None
        self.assertEqual(loaded.rels_ext.about, 'info:fedora/example:42')
        self.assertEqual([member.name for member in loaded.rels_ext.is_member_of], ['info:fedora/example:collection'])
        self.assertEqual([stream.id for stream in loaded.datastream], ['DC', 'RELS-EXT'])
        self.assertEqual(second.serialize(), unchanged)

    def test_darwin_core_field_removal_preserves_namespaces_and_other_values(self) -> None:
        """
        Checks generated fields write to the correct namespaces and optional values can be removed.
        """
        container = darwincore.make_simple_darwin_record_set()
        container.create_simple_darwin_record()
        record = container.simple_darwin_record
        assert record is not None
        record.type_ = 'PhysicalObject'
        record.class_ = 'Aves'
        record.catalog_number = 'CAT & <42>'
        record.event_id = 'event:42'
        edited = darwincore.SimpleDarwinRecordSet(node=etree.fromstring(container.serialize()))
        assert edited.simple_darwin_record is not None
        self.assertEqual(edited.simple_darwin_record.catalog_number, 'CAT & <42>')
        edited.simple_darwin_record.catalog_number = None

        loaded = darwincore.SimpleDarwinRecordSet(node=etree.fromstring(edited.serialize()))
        assert loaded.simple_darwin_record is not None
        node = loaded.simple_darwin_record.node
        self.assertEqual(node.findtext('{http://purl.org/dc/terms/}type'), 'PhysicalObject')
        self.assertEqual(node.findtext('{http://rs.tdwg.org/dwc/terms/}class'), 'Aves')
        self.assertEqual(node.findtext('{http://rs.tdwg.org/dwc/terms/}eventID'), 'event:42')
        self.assertIsNone(node.find('{http://rs.tdwg.org/dwc/terms/}catalogNumber'))
        self.assertIsNone(loaded.simple_darwin_record.catalog_number)
        self.assertEqual(loaded.validation_errors(), [])
