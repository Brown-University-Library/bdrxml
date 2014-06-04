# coding: utf-8
import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml import mods

SAMPLE_MODS = u'''
<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ID="id101" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd">
  <mods:titleInfo>
    <mods:title>Poétry</mods:title>
  </mods:titleInfo>
  <mods:titleInfo>
    <mods:title>Other title</mods:title>
  </mods:titleInfo>
  <mods:titleInfo type="alternative" displayLabel="First line">
    <mods:title>alternative title</mods:title>
  </mods:titleInfo>
  <mods:accessCondition href="http://creativecommons.org/publicdomain/zero/1.0/" type="use and reproduction">To the extent possible under law, the person who associated CC0 with this work has waived all copyright and related or neighboring rights to this work.</mods:accessCondition>
  <mods:accessCondition href="http://i.creativecommons.org/p/zero/1.0/88x31.png" type="logo"></mods:accessCondition>
  <mods:identifier type="test type">Test type id</mods:identifier>
  <mods:identifier displayLabel="label">label id</mods:identifier>
  <mods:identifier type="doi">dx.123.456</mods:identifier>
  <mods:name type="personal">
    <mods:namePart></mods:namePart>
  </mods:name>
  <mods:name type="personal">
    <mods:namePart>Smith, Tom</mods:namePart>
    <mods:namePart type="date">1803 or 4-1860</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">creator</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:originInfo displayLabel="date added">
    <mods:place><mods:placeTerm>USA</mods:placeTerm></mods:place>
    <mods:dateCreated encoding="w3cdtf" qualifier="questionable">2018-01</mods:dateCreated>
    <mods:copyrightDate encoding="w3cdtf" keyDate="yes">2008</mods:copyrightDate>
    <mods:dateCreated encoding="w3cdtf" keyDate="yes"></mods:dateCreated>
    <mods:dateCreated encoding="w3cdtf" keyDate="yes">2008-02-03</mods:dateCreated>
    <mods:dateModified encoding="w3cdtf">2008-06-07-2009-01-02</mods:dateModified>
    <mods:dateModified encoding="w3cdtf" point="start">invalid date</mods:dateModified>
    <mods:dateModified encoding="w3cdtf" point="start">2008-05-06</mods:dateModified>
    <mods:dateModified encoding="w3cdtf" point="start">2008-06-07</mods:dateModified>
    <mods:dateOther encoding="w3cdtf" point="start">2009-10-11</mods:dateOther>
  </mods:originInfo>
  <mods:physicalDescription>
    <mods:extent>viii, 208 p.</mods:extent>
    <mods:digitalOrigin>born digital</mods:digitalOrigin>
    <mods:note>note 1</mods:note>
  </mods:physicalDescription>
  <mods:note>Thésis (Ph.D.)</mods:note>
  <mods:note type="@#$%random Typé" displayLabel="discarded:">random type note</mods:note>
  <mods:note displayLabel="Short">Without ending</mods:note>
  <mods:note displayLabel="Display @#$label?">display label note</mods:note>
  <mods:name type="personal">
    <mods:namePart>Baker, Jim</mods:namePart>
    <mods:namePart type="date">1718-1762</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">director</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:name type="personal">
    <mods:namePart>Wilson, Jane</mods:namePart>
  </mods:name>
  <mods:name type="corporate">
    <mods:namePart>Brown University. English</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">sponsor</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:name type="corporate">
    <mods:namePart>Providence, RI</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">distribution place</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:typeOfResource>text</mods:typeOfResource>
  <mods:genre authority="aat"></mods:genre>
  <mods:genre authority="aat">aat theses</mods:genre>
  <mods:genre authority="bdr">bdr theses</mods:genre>
  <mods:genre authority="local">local theses</mods:genre>
  <mods:abstract>Poétry description...</mods:abstract>
  <mods:subject displayLabel="Display Labél!">
    <mods:topic>modernism</mods:topic>
  </mods:subject>
  <mods:subject>
    <mods:topic>metalepsis</mods:topic>
  </mods:subject>
  <mods:subject displayLabel="Display Label:">
    <mods:topic>Yeats</mods:topic>
  </mods:subject>
  <mods:subject authority="local">
    <mods:topic>Ted</mods:topic>
    <mods:topic>Stevens</mods:topic>
  </mods:subject>
  <mods:subject>
    <mods:topic>Merrill</mods:topic>
  </mods:subject>
  <mods:subject authority="local">
    <mods:topic>Eliot</mods:topic>
  </mods:subject>
  <mods:subject authority="local">
    <mods:hierarchicalGeographic>
      <mods:country>United States</mods:country>
      <mods:state>Louisiana</mods:state>
      <mods:city>New Orleans</mods:city>
      <mods:citySection>Lower Ninth Ward</mods:citySection>
    </mods:hierarchicalGeographic>
  </mods:subject>
  <mods:subject displayLabel="label missing colon">
    <mods:topic>post modernism</mods:topic>
  </mods:subject>
  <mods:subject authority="local" displayLabel="label">
    <mods:temporal encoding="w3cdtf">1960s</mods:temporal>
  </mods:subject>
  <mods:recordInfo>
    <mods:recordContentSource authority="marcorg">RPB</mods:recordContentSource>
    <mods:recordCreationDate encoding="iso8601">20091218</mods:recordCreationDate>
  </mods:recordInfo>
  <mods:identifier type="METSID">12345678</mods:identifier>
  <mods:location>
    <mods:physicalLocation>Random location</mods:physicalLocation>
    <mods:holdingSimple>
      <mods:copyInformation>
        <mods:note>location note</mods:note>
      </mods:copyInformation>
    </mods:holdingSimple>
  </mods:location>
  <mods:relatedItem type="host">
        <mods:identifier type="type"></mods:identifier>
        <mods:identifier>test_id</mods:identifier>
        <mods:identifier type="type">1234567890123456</mods:identifier>
        <mods:part>
            <mods:detail type="divid">
                <mods:number>div01</mods:number>
            </mods:detail>
        </mods:part>
    </mods:relatedItem>
</mods:mods>
'''
CREATE_MODS = u'''<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd">
  <mods:titleInfo>
    <mods:title>Poétry</mods:title>
  </mods:titleInfo>
</mods:mods>
'''

class ModsReadWrite(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.mods = mods.make_mods()
        
    def test_load_sample_mods(self):
        loaded = load_xmlobject_from_string(SAMPLE_MODS, mods.Mods)
        self.assertEqual(loaded.id, 'id101')
        self.assertEqual(loaded.title, u'Poétry')
        self.assertEqual(loaded.title_info[1].title, 'Other title')
        self.assertEqual(loaded.title_info[2].title, 'alternative title')
        self.assertEqual(loaded.title_info[2].type, 'alternative')
        self.assertEqual(loaded.title_info[2].label, 'First line')
        self.assertEqual(loaded.origin_info.label, 'date added')
        self.assertEqual(loaded.origin_info.places[0].place_terms[0].text, u'USA')

        #test names
        personal_names = [unicode(name.name_parts[0].text) for name in loaded.names if name.type == 'personal' and name.name_parts[0].text]
        self.assertEqual(len(personal_names), 3)
        personal_name_list = [u'Smith, Tom', u'Baker, Jim', u'Wilson, Jane']
        for i in range(3):
            self.assertTrue(personal_names[i] in personal_name_list)
        corporate_names = [unicode(name) for name in loaded.names if name.type == 'corporate']
        corporate_name_list = [u'Brown University. English', 'Providence, RI']
        self.assertEqual(corporate_names, corporate_name_list)

        self.assertEqual(loaded.resource_type, 'text')
        self.assertEqual(loaded.genres[1].text, 'aat theses')
        self.assertEqual(loaded.notes[0].text, u'Thésis (Ph.D.)')
        self.assertEqual(loaded.physical_description.extent, u'viii, 208 p.')
        self.assertEqual(loaded.physical_description.digital_origin, u'born digital')
        self.assertEqual(loaded.physical_description.note, u'note 1')
        self.assertEqual(loaded.locations[0].physical, u'Random location')
        self.assertEqual(loaded.locations[0].holding_simple.copy_information[0].notes[0].text, u'location note')

    def test_create_mods(self):
        self.mods.title = u'Poétry'
        self.assertEqual(unicode(self.mods.serialize(pretty=True), 'utf-8'), CREATE_MODS)

    def test_round_trip(self):
        self.mods.title = "Sample title"
        self.mods.create_origin_info()
        self.mods.origin_info.publisher = "BUL"
        mods_str = self.mods.serialize(pretty=False)
        loaded = load_xmlobject_from_string(mods_str, mods.Mods)
        self.assertEqual(loaded.title, 'Sample title')
        self.assertEqual(loaded.origin_info.publisher, 'BUL')

    def test_subjects(self):
        self.mods.title = "Sample"
        topics = ['sample', 'test']
        for keyword in topics:
            self.mods.subjects.append(mods.Subject(topic=keyword))
        new_mods = load_xmlobject_from_string(self.mods.serialize(), mods.Mods)
        self.assertEqual(topics, [s.topic for s in new_mods.subjects])

    def test_create_dates(self):
        other_date = mods.DateOther(type='random', date='2013-01-03')
        create_date = mods.DateCreated(date='2012-12-12')
        modified_date = mods.DateModified(date='2011-11-11')
        origin_info = mods.OriginInfo()
        origin_info.other.append(other_date)
        origin_info.created.append(create_date)
        origin_info.modified.append(modified_date)
        self.assertEqual(origin_info.other[0].date, '2013-01-03')
        self.assertEqual(origin_info.created[0].date, '2012-12-12')
        self.assertEqual(origin_info.modified[0].date, '2011-11-11')

    def test_create_hierarchical_geographic(self):
        hg = mods.HierarchicalGeographic(
                country='United States',
                state='Louisiana',
                city='New Orleans',
                city_section='Lower Ninth Ward')
        subject = mods.Subject(authority='local', hierarchical_geographic=hg)
        self.assertEqual(subject.hierarchical_geographic.country, 'United States')
        self.assertEqual(subject.hierarchical_geographic.state, 'Louisiana')
        self.assertEqual(subject.hierarchical_geographic.city, 'New Orleans')
        self.assertEqual(subject.hierarchical_geographic.city_section, 'Lower Ninth Ward')

    def test_geographic_subjects(self):
        loaded = load_xmlobject_from_string(SAMPLE_MODS, mods.Mods)
        subject = loaded.subjects[-3]
        self.assertEqual(subject.hierarchical_geographic.country, 'United States')
        self.assertEqual(subject.hierarchical_geographic.state, 'Louisiana')
        self.assertEqual(subject.hierarchical_geographic.city, 'New Orleans')
        self.assertEqual(subject.hierarchical_geographic.city_section, 'Lower Ninth Ward')

    def test_index_data(self):
        loaded = load_xmlobject_from_string(SAMPLE_MODS, mods.Mods)
        index_data = mods.ModsIndexer(loaded).index_data()
        self.assertEqual(index_data['abstract'], [u'Poétry description...'])
        self.assertEqual(index_data['contributor_display'], ['Smith, Tom, 1803 or 4-1860 (creator)', 'Baker, Jim, 1718-1762 (director)', 'Wilson, Jane', 'Brown University. English (sponsor)', 'Providence, RI (distribution place)'])
        self.assertEqual(index_data['copyrightDate'], '2008-01-01T00:00:00Z')
        self.assertEqual(index_data['copyrightDate_year_ssim'], ['2008'])
        self.assertEqual(index_data['dateCreated'], '2008-02-03T00:00:00Z')
        self.assertEqual(sorted(index_data['dateCreated_year_ssim']), ['2008'])
        self.assertEqual(index_data['dateModified'], '2008-05-06T00:00:00Z')
        self.assertEqual(index_data['dateModified_year_ssim'], ['2008', '2008'])
        self.assertEqual(index_data['dateModified_ssim'], ['2008-06-07-2009-01-02', 'invalid date', '2008-06-07'])
        self.assertEqual(index_data['genre'], [u'aat theses', u'bdr theses', u'local theses'])
        self.assertEqual(index_data['identifier'], [u'Test type id', u'label id'])
        self.assertEqual(index_data['mods_genre_aat_ssim'], [u'aat theses'])
        self.assertEqual(index_data['mods_genre_bdr_ssim'], [u'bdr theses'])
        self.assertEqual(index_data['mods_genre_local_ssim'], [u'local theses'])
        self.assertEqual(index_data['mods_access_condition_logo_ssim'], [u'http://i.creativecommons.org/p/zero/1.0/88x31.png'])
        self.assertEqual(index_data['mods_access_condition_use_text_tsim'], [u'To the extent possible under law, the person who associated CC0 with this work has waived all copyright and related or neighboring rights to this work.'])
        self.assertEqual(index_data['mods_access_condition_use_link_ssim'], [u'http://creativecommons.org/publicdomain/zero/1.0/'])
        self.assertEqual(index_data['mods_id'], 'id101')
        self.assertEqual(index_data['mods_id_test_type_ssim'], ['Test type id'])
        self.assertEqual(index_data['mods_id_doi_ssi'], 'dx.123.456')
        self.assertEqual(index_data['mods_id_label_ssim'], ['label id'])
        self.assertEqual(index_data['mods_physicalDescription_extent_ssim'], [u'viii, 208 p.'])
        self.assertEqual(index_data['mods_physicalDescription_digitalOrigin_ssim'], [u'born digital'])
        self.assertEqual(index_data['mods_name_place_ssim'], [u'Providence, RI'])
        self.assertEqual(sorted(index_data['mods_name_nonplace_ssim']), [u'Baker, Jim', u'Brown University. English', u'Smith, Tom', u'Wilson, Jane'])
        self.assertEqual(sorted(index_data['mods_role_ssim']), [u'creator', u'director', u'distribution place', u'sponsor'])
        self.assertEqual(index_data['mods_related_id_ssim'], ['test_id'])
        self.assertEqual(index_data['mods_related_id_type_ssim'], ['1234567890123456'])
        self.assertEqual(index_data['mods_role_creator_ssim'], [u'Smith, Tom'])
        self.assertEqual(index_data['mods_role_director_ssim'], [u'Baker, Jim'])
        self.assertEqual(index_data['mods_role_sponsor_ssim'], [u'Brown University. English'])
        self.assertEqual(index_data['mods_note_random_type_ssim'], [u'random type note'])
        self.assertEqual(index_data['mods_note_discarded_ssim'], [u'random type note'])
        self.assertEqual(index_data['mods_note_display_label_ssim'], [u'display label note'])
        self.assertEqual(index_data['mods_title_alt'], [u'alternative title'])
        self.assertEqual(index_data['name'], [u'Smith, Tom', u'Baker, Jim', u'Wilson, Jane', u'Brown University. English', u'Providence, RI'])
        self.assertEqual(index_data['note'], [u'Thésis (Ph.D.)', u'discarded: random type note', u'Short: Without ending', u'Display @#$label? display label note'])
        self.assertEqual(index_data['other_title'], [u'Other title'])
        self.assertEqual(index_data['primary_title'], u'Poétry')
        self.assertEqual(index_data['keyword'], [u'Display Labél! modernism', u'metalepsis', u'Display Label: Yeats', u'Ted', u'Stevens', u'Merrill', u'Eliot', u"label missing colon: post modernism", u'label: 1960s'])
        self.assertEqual(index_data['mods_subject_ssim'], [u'Display Labél! modernism', u'metalepsis', u'Display Label: Yeats', u'Ted', u'Stevens', u'Merrill', u'Eliot', u"label missing colon: post modernism", u'label: 1960s'])
        self.assertEqual(index_data['mods_subject_display_label_ssim'], [u'modernism', u'Yeats'])
        self.assertEqual(index_data['mods_subject_label_ssim'], [u'1960s'])
        self.assertEqual(index_data['mods_subject_label_missing_colon_ssim'], [u'post modernism'])
        self.assertEqual(index_data['mods_subject_local_ssim'], [u'Ted', u'Stevens', u'Eliot', u'label: 1960s'])

    def test_index_title_parts(self):
        loaded = load_xmlobject_from_string(SAMPLE_MODS, mods.Mods)
        primary_title = loaded.title_info_list[0]
        primary_title.subtitle = "Primary Subtitle"
        primary_title.part_name = "Primary Part 1"
        primary_title.part_number = "4"
        primary_title.non_sort  = "The"
        index_data = mods.ModsIndexer(loaded).index_data()
        self.assertEqual(index_data['subtitle'], u'Primary Subtitle')
        self.assertEqual(index_data['partnumber'], u'4')
        self.assertEqual(index_data['partname'], u'Primary Part 1')
        self.assertEqual(index_data['nonsort'], u'The')



def suite():
    suite = unittest.makeSuite(ModsReadWrite, 'test')
    return suite


if __name__ == '__main__':
    unittest.main()

