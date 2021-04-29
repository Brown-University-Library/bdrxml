# coding: utf-8
from __future__ import unicode_literals
import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml import mods

SAMPLE_MODS = '''
<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ID="id101" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd">
  <mods:titleInfo>
    <mods:title>Poétry
    Title</mods:title>
  </mods:titleInfo>
  <mods:titleInfo>
    <mods:title>Other title</mods:title>
  </mods:titleInfo>
  <mods:titleInfo type="alternative" displayLabel="First line">
    <mods:title>alternative title</mods:title>
  </mods:titleInfo>
  <mods:accessCondition xlink:href="http://creativecommons.org/publicdomain/zero/1.0/" type="use and reproduction">To the extent possible under law, the person who associated CC0 with this work has waived all copyright and related or neighboring rights to this work.</mods:accessCondition>
  <mods:accessCondition xlink:href="http://i.creativecommons.org/xlink.png" type="logo"></mods:accessCondition>
  <mods:identifier type="test type">Test type id</mods:identifier>
  <mods:identifier displayLabel="label">label id</mods:identifier>
  <mods:identifier type="doi">dx.123.456</mods:identifier>
  <mods:name type="personal">
    <mods:namePart></mods:namePart>
  </mods:name>
  <mods:name type="personal" authority="fast" authorityURI="http://fast.com" valueURI="http://fast.com/1">
    <mods:namePart>Smith, Tom</mods:namePart>
    <mods:namePart type="date">1803 or 4-1860</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text" authority="marcrelator" authorityURI="http://id.loc.gov/vocabulary/relators" valueURI="http://id.loc.gov/vocabulary/relators/cre">Creator</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:targetAudience authority="local">Target Audience</mods:targetAudience>
  <mods:originInfo displayLabel="date added">
    <mods:place><mods:placeTerm authority="auth" authorityURI="http://auth.com" valueURI="http://auth.com/usa">USA</mods:placeTerm></mods:place>
    <mods:dateCreated encoding="w3cdtf" qualifier="questionable">2018-01</mods:dateCreated>
    <mods:copyrightDate encoding="w3cdtf" keyDate="yes">2008</mods:copyrightDate>
    <mods:dateCreated encoding="w3cdtf" keyDate="yes"></mods:dateCreated>
    <mods:dateCreated encoding="w3cdtf" keyDate="yes">2008-02-03</mods:dateCreated>
    <mods:dateIssued encoding="w3cdtf" point="end">2008-04-25</mods:dateIssued>
    <mods:dateModified encoding="w3cdtf">2008-06-07-2009-01-02</mods:dateModified>
    <mods:dateModified encoding="w3cdtf" point="start">invalid date</mods:dateModified>
    <mods:dateModified encoding="w3cdtf" point="start">2008-05-06</mods:dateModified>
    <mods:dateModified encoding="w3cdtf" point="start">2008-06-07</mods:dateModified>
    <mods:dateOther encoding="w3cdtf" qualifier="inferred">2000</mods:dateOther>
    <mods:dateOther encoding="w3cdtf" qualifier="approximate">2009</mods:dateOther>
  </mods:originInfo>
  <mods:physicalDescription>
    <mods:extent>viii, 208 p.</mods:extent>
    <mods:digitalOrigin>born digital</mods:digitalOrigin>
    <mods:note>note 1</mods:note>
    <mods:form type="material">oil</mods:form>
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
  <mods:language>
    <mods:languageTerm authority="iso639-2b" authorityURI="http://id.loc.gov/vocabulary/iso639-2.html" valueURI="http://id.loc.gov/vocabulary/iso639-2/eng">English</mods:languageTerm>
  </mods:language>
  <mods:genre authority="aat"></mods:genre>
  <mods:genre authority="aat">aat theses</mods:genre>
  <mods:genre authority="bdr">bdr theses</mods:genre>
  <mods:genre authority="local">local theses</mods:genre>
  <mods:genre authority="fast" authorityURI="http://fast.com" valueURI="http://fast.com/123">123</mods:genre>
  <mods:genre type="object type" authority="aat">sherd</mods:genre>
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
  <mods:subject authority="fast" authorityURI="http://fast.com" valueURI="http://fast.com/456">
    <mods:topic>456</mods:topic>
  </mods:subject>
  <mods:recordInfo>
    <mods:recordContentSource authority="marcorg">RPB</mods:recordContentSource>
    <mods:recordCreationDate encoding="iso8601">20091218</mods:recordCreationDate>
    <mods:recordIdentifier source="RPB">a1234567</mods:recordIdentifier>
  </mods:recordInfo>
  <mods:classification displayLabel="Test classification" authority="classauth" authorityURI="http://classauth.com" valueURI="http://classauth.com/some">Some classification</mods:classification>
  <mods:identifier type="METSID">12345678</mods:identifier>
  <mods:location>
    <mods:physicalLocation authority="locauth" authorityURI="http://locauth.com" valueURI="http://locauth.com/random">Random location</mods:physicalLocation>
    <mods:holdingSimple>
      <mods:copyInformation>
        <mods:note>location note</mods:note>
        <mods:subLocation>Bishop Collection</mods:subLocation>
      </mods:copyInformation>
    </mods:holdingSimple>
  </mods:location>
  <mods:relatedItem type="host">
    <mods:identifier type="type"></mods:identifier>
    <mods:identifier>test_id</mods:identifier>
    <mods:dateCreated encoding="w3cdtf" keyDate="yes">1908-04-03</mods:dateCreated>
    <mods:identifier type="type">1234567890123456</mods:identifier>
    <mods:part>
      <mods:detail type="divid">
        <mods:number>div01</mods:number>
      </mods:detail>
    </mods:part>
    <mods:name type="personal">
      <mods:namePart>Shakespeare, William</mods:namePart>
    </mods:name>
  </mods:relatedItem>
  <mods:relatedItem displayLabel="location of original">
    <mods:classification displayLabel="label">Classification</mods:classification>
  </mods:relatedItem>
</mods:mods>
'''
MODS_35_XML = '''
<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd" ID="id101" version="3.5">
    <mods:titleInfo>
        <mods:title>A Title</mods:title>
    </mods:titleInfo>
</mods:mods>
'''
INVALID_MODS_XML = '''
<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-7.xsd" ID="id101" version="3.7">
    <mods:titleInfo>
        <mods:random>A Title</mods:random>
    </mods:titleInfo>
</mods:mods>
'''
MODS_SNIPPET = '''
  <mods:titleInfo>
    <mods:title>Poétry</mods:title>
  </mods:titleInfo>
</mods:mods>
'''
MODS_TEMPLATE = u'''
      <mods:mods ID="id101"
         xmlns:mods="http://www.loc.gov/mods/v3"
         xmlns:xlink="http://www.w3.org/1999/xlink"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd">
         {inserted_mods}
      </mods:mods>
'''


class ModsReadWrite(unittest.TestCase):

    def mods_from_partial(self, mods_partial):
        sample_mods = MODS_TEMPLATE.format(inserted_mods=mods_partial)
        return load_xmlobject_from_string(sample_mods, mods.Mods)

    def setUp(self):
        #basic mods
        self.mods = mods.make_mods()

    def test_load_sample_mods(self):
        loaded = load_xmlobject_from_string(SAMPLE_MODS, mods.Mods)
        self.assertEqual(loaded.id, 'id101')
        self.assertEqual(loaded.title, 'Poétry\n    Title')
        self.assertEqual(loaded.title_info[1].title, 'Other title')
        self.assertEqual(loaded.title_info[2].title, 'alternative title')
        self.assertEqual(loaded.title_info[2].type, 'alternative')
        self.assertEqual(loaded.title_info[2].label, 'First line')
        self.assertEqual(loaded.origin_info.label, 'date added')
        self.assertEqual(loaded.origin_info.places[0].place_terms[0].text, 'USA')
        self.assertEqual(loaded.origin_info.places[0].place_terms[0].authority, 'auth')
        self.assertEqual(loaded.origin_info.places[0].place_terms[0].authority_uri, 'http://auth.com')
        self.assertEqual(loaded.origin_info.places[0].place_terms[0].value_uri, 'http://auth.com/usa')

        #test names
        personal_names = [name.name_parts[0].text for name in loaded.names if name.type == 'personal' and name.name_parts[0].text]
        self.assertEqual(len(personal_names), 3)
        personal_name_list = ['Smith, Tom', 'Baker, Jim', 'Wilson, Jane']
        for i in range(3):
            self.assertTrue(personal_names[i] in personal_name_list)
        corporate_names = [name.name_parts[0].text for name in loaded.names if name.type == 'corporate']
        corporate_name_list = ['Brown University. English', 'Providence, RI']
        self.assertEqual(corporate_names, corporate_name_list)
        tom_smith = [name for name in loaded.names if name.name_parts[0].text == 'Smith, Tom'][0]
        self.assertEqual(tom_smith.authority, 'fast')
        self.assertEqual(tom_smith.authority_uri, 'http://fast.com')
        self.assertEqual(tom_smith.value_uri, 'http://fast.com/1')
        self.assertEqual(tom_smith.roles[0].authority, 'marcrelator')
        self.assertEqual(tom_smith.roles[0].authority_uri, 'http://id.loc.gov/vocabulary/relators')
        self.assertEqual(tom_smith.roles[0].value_uri, 'http://id.loc.gov/vocabulary/relators/cre')

        self.assertEqual(loaded.resource_type, 'text')
        self.assertEqual(loaded.genres[1].text, 'aat theses')
        self.assertEqual(loaded.genres[4].text, '123')
        self.assertEqual(loaded.genres[4].authority, 'fast')
        self.assertEqual(loaded.genres[4].authority_uri, 'http://fast.com')
        self.assertEqual(loaded.genres[4].value_uri, 'http://fast.com/123')
        self.assertEqual(loaded.genres[5].text, 'sherd')
        self.assertEqual(loaded.genres[5].type, 'object type')
        s = [s for s in loaded.subjects if s.topic == '456'][0]
        self.assertEqual(s.authority, 'fast')
        self.assertEqual(s.authority_uri, 'http://fast.com')
        self.assertEqual(s.value_uri, 'http://fast.com/456')
        self.assertEqual(loaded.notes[0].text, 'Thésis (Ph.D.)')
        self.assertEqual(loaded.target_audiences[0].text, 'Target Audience')
        self.assertEqual(loaded.target_audiences[0].authority, 'local')
        self.assertEqual(loaded.physical_description.extent, 'viii, 208 p.')
        self.assertEqual(loaded.physical_description.digital_origin, 'born digital')
        self.assertEqual(loaded.physical_description.note, 'note 1')
        self.assertEqual(loaded.languages[0].terms[0].authority, 'iso639-2b')
        self.assertEqual(loaded.languages[0].terms[0].authority_uri, 'http://id.loc.gov/vocabulary/iso639-2.html')
        self.assertEqual(loaded.languages[0].terms[0].value_uri, 'http://id.loc.gov/vocabulary/iso639-2/eng')
        self.assertEqual(loaded.classifications[0].text, 'Some classification')
        self.assertEqual(loaded.classifications[0].label, 'Test classification')
        self.assertEqual(loaded.classifications[0].authority, 'classauth')
        self.assertEqual(loaded.classifications[0].authority_uri, 'http://classauth.com')
        self.assertEqual(loaded.classifications[0].value_uri, 'http://classauth.com/some')
        self.assertEqual(loaded.locations[0].physical.text, 'Random location')
        self.assertEqual(loaded.locations[0].physical.authority, 'locauth')
        self.assertEqual(loaded.locations[0].physical.authority_uri, 'http://locauth.com')
        self.assertEqual(loaded.locations[0].physical.value_uri, 'http://locauth.com/random')
        self.assertEqual(loaded.locations[0].holding_simple.copy_information[0].notes[0].text, 'location note')
        self.assertEqual(loaded.locations[0].holding_simple.copy_information[0].sublocations[0].text, 'Bishop Collection')
        self.assertEqual(loaded.record_info_list[0].record_identifier_list[0].source, 'RPB')
        self.assertEqual(loaded.record_info_list[0].record_identifier_list[0].text, 'a1234567')
        self.assertEqual(loaded.record_info_list[0].record_creation_date.date, '20091218')
        self.assertEqual(loaded.record_info_list[0].record_creation_date.encoding, 'iso8601')
        self.assertEqual(loaded.record_info_list[0].record_content_source.text, 'RPB')
        self.assertEqual(loaded.record_info_list[0].record_content_source.authority, 'marcorg')
        self.assertEqual(loaded.related_items[1].label, 'location of original')
        self.assertEqual(loaded.related_items[1].classifications[0].text, 'Classification')

    def test_create_mods(self):
        self.mods.title = 'Poétry'
        self.assertTrue(MODS_SNIPPET.encode('utf8') in self.mods.serialize(pretty=True))
        self.assertTrue(self.mods.is_valid())

    def test_round_trip(self):
        self.mods.title = "Sample title"
        self.mods.create_origin_info()
        self.mods.origin_info.publisher = "BUL"
        mods_str = self.mods.serialize(pretty=False)
        loaded = load_xmlobject_from_string(mods_str, mods.Mods)
        self.assertEqual(loaded.title, 'Sample title')
        self.assertEqual(loaded.origin_info.publisher, 'BUL')

    def test_setting_xlink_href(self):
        access_condition = mods.AccessCondition(text='access condition')
        access_condition.node.set('{%s}href' % mods.XLINK_NAMESPACE, 'http://example.com')
        self.mods.access_conditions.append(access_condition)
        mods_str = self.mods.serialize(pretty=False)
        loaded = load_xmlobject_from_string(mods_str, mods.Mods)
        xlink_href = loaded.access_conditions[0].node.get('{%s}href' % mods.XLINK_NAMESPACE)
        self.assertEqual(xlink_href, 'http://example.com')

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
        subject = [s for s in loaded.subjects if s.hierarchical_geographic][0]
        self.assertEqual(subject.hierarchical_geographic.country, 'United States')
        self.assertEqual(subject.hierarchical_geographic.state, 'Louisiana')
        self.assertEqual(subject.hierarchical_geographic.city, 'New Orleans')
        self.assertEqual(subject.hierarchical_geographic.city_section, 'Lower Ninth Ward')

    def test_parts(self):
        sample_mods = u'''
           <mods:part>
               <mods:detail type="issue">
                   <mods:number>11</mods:number>
                   <mods:caption>no.</mods:caption>
               </mods:detail>
               <mods:extent unit="pages">
                   <mods:start>735</mods:start>
                   <mods:end>743</mods:end>
                   <mods:total>8</mods:total>
               </mods:extent>
           </mods:part>
        '''
        loaded = self.mods_from_partial(sample_mods)
        part = loaded.parts[0]
        self.assertEqual(part.details[0].number, '11')
        self.assertEqual(part.details[0].caption, 'no.')

    def test_create_language(self):
        lang = mods.Language()
        lang.terms.append(mods.LanguageTerm(text='English'))
        self.mods.languages.append(lang)
        self.assertTrue(self.mods.is_valid())

    def test_validate_mods_35(self):
        loaded = load_xmlobject_from_string(MODS_35_XML, mods.Mods)
        self.assertTrue(loaded.is_valid())

    def test_validate_created_mods(self):
        self.mods.title = 'Poétry'
        self.assertTrue(self.mods.is_valid())

    def test_invalid(self):
        loaded = load_xmlobject_from_string(INVALID_MODS_XML, mods.Mods)
        self.assertFalse(loaded.is_valid())

    def test_mods_add_topic(self):
        mods_obj = mods.make_mods()
        mods_obj.title = 'title'
        mods.add_topic(mods_obj, 'random')
        self.assertEqual(mods_obj.subjects[0].topic, 'random')

    def test_mods_add_topic_label_and_fast(self):
        mods_obj = mods.make_mods()
        mods_obj.title = 'title'
        mods.add_topic(mods_obj, 'random', label='Label:', fast_uri='http://id.worldcat.org/fast/902025')
        self.assertEqual(mods_obj.subjects[0].topic, 'random')
        self.assertEqual(mods_obj.subjects[0].label, 'Label:')
        self.assertEqual(mods_obj.subjects[0].value_uri, 'http://id.worldcat.org/fast/902025')
        self.assertEqual(mods_obj.subjects[0].authority_uri, 'http://id.worldcat.org/fast')
        self.assertEqual(mods_obj.subjects[0].authority, 'fast')

    def test_mods_add_topic_already_exists(self):
        #if the topic already exists, just return and don't do anything
        mods_obj = mods.make_mods()
        mods_obj.title = 'title'
        mods_obj.subjects.append(mods.Subject(topic='random'))
        mods.add_topic(mods_obj, 'random')
        self.assertEqual(len(mods_obj.subjects), 1)
        self.assertEqual(mods_obj.subjects[0].topic, 'random')

    def test_mods_add_topic_incompatible(self):
        #if topic is there, but with different label or authority info, raise an exception
        mods_obj = mods.make_mods()
        mods_obj.title = 'title'
        mods_obj.subjects.append(mods.Subject(topic='random', label='label1'))
        with self.assertRaises(Exception) as cm:
            mods.add_topic(mods_obj, 'random', label='label2')
        self.assertEqual(str(cm.exception), 'mods object already has topic "random"')

    def test_mods_add_topic_partial(self):
        #if topic is partially there, finish adding whatever's missing
        mods_obj = mods.make_mods()
        mods_obj.title = 'title'
        mods_obj.subjects.append(mods.Subject(topic='random', label='label1'))
        mods.add_topic(mods_obj, 'random', label='label1', fast_uri='http://id.worldcat.org/fast/902025')
        self.assertEqual(len(mods_obj.subjects), 1)
        s = mods_obj.subjects[0]
        self.assertEqual(s.topic, 'random')
        self.assertEqual(s.label, 'label1')
        self.assertEqual(s.authority, 'fast')
        self.assertEqual(s.authority_uri, 'http://id.worldcat.org/fast')
        self.assertEqual(s.value_uri, 'http://id.worldcat.org/fast/902025')

    def test_fast_uri_equality(self):
        self.assertTrue(mods._fast_uris_equal('http://id.worldcat.org/fast/902025', 'http://id.worldcat.org/fast/902025'))
        self.assertFalse(mods._fast_uris_equal('http://id.worldcat.org/fast/902025', 'http://id.worldcat.org/fast/902026'))
        self.assertTrue(mods._fast_uris_equal('http://id.worldcat.org/fast/00902025', 'http://id.worldcat.org/fast/902025'))
        self.assertTrue(mods._fast_uris_equal('http://id.worldcat.org/fast/00902025/', 'http://id.worldcat.org/fast/902025/'))
        self.assertTrue(mods._fast_uris_equal('http://id.worldcat.org/fast/902025/', 'http://id.worldcat.org/fast/902025/'))
        self.assertFalse(mods._fast_uris_equal('http://id.worldcat.org/fast/902025/', 'http://id.worldcat.org/fast/902026/'))


def suite():
    suite = unittest.makeSuite(ModsReadWrite, 'test')
    return suite


if __name__ == '__main__':
    unittest.main()

