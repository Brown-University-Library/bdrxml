import unittest
from eulxml.xmlmap  import load_xmlobject_from_string
from bdrxml.mods import Mods, make_mods, MODS_SCHEMA, LocalTopic

#sample MODS from bdr:10 on DAXDEV
SAMPLE_MODS = '''
<mods:mods xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ID="etd100" xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd">
  <mods:titleInfo>
    <mods:title>Time Travels: Metalepsis and Modernist Poetry</mods:title>
  </mods:titleInfo>
  <mods:name type="personal">
    <mods:namePart>Ben-Merre, David N.</mods:namePart>
    <mods:role>
      <mods:roleTerm type="text">creator</mods:roleTerm>
    </mods:role>
  </mods:name>
  <mods:originInfo>
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
  <mods:recordInfo>
    <mods:recordContentSource authority="marcorg">RPB</mods:recordContentSource>
    <mods:recordCreationDate encoding="iso8601">20091218</mods:recordCreationDate>
  </mods:recordInfo>
</mods:mods>
'''

class ModsReadWrite(unittest.TestCase):
    def setUp(self):
        #basic fox
        self.mods = make_mods()
        
    def test_sample_mods(self):
        loaded = load_xmlobject_from_string(SAMPLE_MODS, Mods)
        self.assertEqual(loaded.title, 'Time Travels: Metalepsis and Modernist Poetry')

        #test names
        personal_names = loaded.personal_name
        personal_name_list = ['Ben-Merre, David N.', 'Blasing, Mutlu', 'Katz, Tamar', 'Keach, William', 'Smith, Barbara']
        self.assertEqual(len(personal_names), 5)
        for i in range(5):
            self.assertTrue(personal_names[i].namePart in personal_name_list)
        corporate_names = loaded.corporate_name
        corporate_name_list = ['Brown University. English']
        self.assertEqual(len(corporate_names), 1)
        self.assertEqual(corporate_names[0].namePart, corporate_name_list[0])

        self.assertEqual(loaded.typeOfResource, 'text')
        self.assertEqual(loaded.genre, 'theses')

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
