import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml import mods

#sample MODS from bdr:10 on DAXDEV
SAMPLE_MODS = '''
<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ID="etd100" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd">
  <mods:titleInfo>
    <mods:title>Time Travels: Metalepsis and Modernist Poetry</mods:title>
  </mods:titleInfo>
  <mods:titleInfo type="alternative" displayLabel="First line">
    <mods:title>alternative title</mods:title>
  </mods:titleInfo>
  <mods:name type="personal">
    <mods:namePart>Ben-Merre, David N.</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">creator</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:originInfo displayLabel="date added">
    <mods:copyrightDate encoding="w3cdtf" keyDate="yes">2008</mods:copyrightDate>
  </mods:originInfo>
  <mods:physicalDescription>
    <mods:extent>viii, 208 p.</mods:extent>
    <mods:digitalOrigin>born digital</mods:digitalOrigin>
  </mods:physicalDescription>
  <mods:note>Thesis (Ph.D.) -- Brown University (2008)</mods:note>
  <mods:name type="personal">
    <mods:namePart>Blasing, Mutlu</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">director</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:name type="personal">
    <mods:namePart>Katz, Tamar</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">reader</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:name type="personal">
    <mods:namePart>Keach, William</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">reader</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:name type="personal">
    <mods:namePart>Smith, Barbara</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">reader</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:name type="corporate">
    <mods:namePart>Brown University. English</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">sponsor</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:typeOfResource>text</mods:typeOfResource>
  <mods:genre authority="aat">theses</mods:genre>
  <mods:abstract>In Time Travels: Metalepsis and Modernist Poetry, I examine how modern notions of time play out rhetorically in the work of Wallace Stevens, W. B. Yeats, James Merrill, and T. S.
      Eliot. I focus not so much on the relationships of literature to cosmological or subjective time but, instead, focus on how literary forms alter how we&apos;ve come to understand cultures of
      temporality, such as what we mean by revision, by a literary memory, or by a lyric subject. The central trope I focus on is metalepsis. Unlike most other tropes, which are generally confined to
      a kind of conceptual space, metaleptic narratives rework presumptions of causality, illogically take what comes later or after and substitute them for what comes before. There is both a positing
      and a negating aspect to this trope. On the one hand, metaleptic narratives assume that history is meaningful?that it is part of some larger picture. But, on the other hand, because of its
      anachronistic nature, it always seems to insist that we question the very same meaningful history that it posits. I turn to this trope, because it helps figure an important paradoxical
      relationship between the ways we talk about history and the ways we talk about forms, as well as because it helps figure a central paradox of modernism: the historical condition of being outside
      the historical.</mods:abstract>
  <mods:subject authority="local">
    <mods:topic>modernism</mods:topic>
  </mods:subject>
  <mods:subject authority="local">
    <mods:topic>metalepsis</mods:topic>
  </mods:subject>
  <mods:subject authority="local">
    <mods:topic>Yeats</mods:topic>
  </mods:subject>
  <mods:subject authority="local">
    <mods:topic>Stevens</mods:topic>
  </mods:subject>
  <mods:subject authority="local">
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
  <mods:recordInfo>
    <mods:recordContentSource authority="marcorg">RPB</mods:recordContentSource>
    <mods:recordCreationDate encoding="iso8601">20091218</mods:recordCreationDate>
  </mods:recordInfo>
</mods:mods>
'''

class ModsReadWrite(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.mods = mods.make_mods()
        
    def test_sample_mods(self):
        loaded = load_xmlobject_from_string(SAMPLE_MODS, mods.Mods)
        self.assertEqual(loaded.id, 'etd100')
        self.assertEqual(loaded.title, 'Time Travels: Metalepsis and Modernist Poetry')
        self.assertEqual(loaded.title_info[1].title, 'alternative title')
        self.assertEqual(loaded.title_info[1].type, 'alternative')
        self.assertEqual(loaded.title_info[1].label, 'First line')
        self.assertEqual(loaded.origin_info.label, 'date added')

        #test names
        personal_names = [unicode(name) for name in loaded.names if name.type == 'personal']
        self.assertEqual(len(personal_names), 5)
        personal_name_list = [u'Ben-Merre, David N.', u'Blasing, Mutlu', u'Katz, Tamar', u'Keach, William', u'Smith, Barbara']
        for i in range(5):
            self.assertTrue(personal_names[i] in personal_name_list)
        corporate_names = [unicode(name) for name in loaded.names if name.type == 'corporate']
        corporate_name_list = [u'Brown University. English']
        self.assertEqual(len(corporate_names), 1)
        self.assertEqual(corporate_names, corporate_name_list)

        self.assertEqual(loaded.resource_type, 'text')
        self.assertEqual(loaded.genres[0].text, 'theses')
        self.assertEqual(loaded.notes[0].text, 'Thesis (Ph.D.) -- Brown University (2008)')

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
        subject = loaded.subjects[-1]
        self.assertEqual(subject.hierarchical_geographic.country, 'United States')
        self.assertEqual(subject.hierarchical_geographic.state, 'Louisiana')
        self.assertEqual(subject.hierarchical_geographic.city, 'New Orleans')
        self.assertEqual(subject.hierarchical_geographic.city_section, 'Lower Ninth Ward')
        

def suite():
    suite = unittest.makeSuite(ModsReadWrite, 'test')
    return suite

if __name__ == '__main__':
    unittest.main()

