import re
import unicodedata
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeListField, NodeField
#import everything from eulxml.xmlmap.mods because clients have to use a lot of
#   those classes, and we're just overriding a few of them here.
from eulxml.xmlmap.mods import *

XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_LOCATION = 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd'

class PlaceTerm(Common):
    ROOT_NAME = 'placeTerm'
    type = SF('@type')
    authority = SF('@authority')
    text = SF('text()')

class Place(Common):
    ROOT_NAME = 'place'
    place_terms = NodeListField('mods:placeTerm', PlaceTerm)

class OriginInfo(OriginInfo):
    label = SF('@displayLabel')
    places = NodeListField('mods:place', Place)


class Collection(RelatedItem):
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')


class PhysicalDescriptionForm(Common):
    ROOT_NAME = 'form'
    authority = SF('@authority')
    type = SF('@type')
    text = SF('text()')

class PhysicalDescription(PhysicalDescription):
    digital_origin = SF('mods:digitalOrigin')
    note = SF('mods:note')
    forms = NodeListField('mods:form', PhysicalDescriptionForm)


class CopyInformation(Common):
    ROOT_NAME = 'copyInformation'
    notes = NodeListField('mods:note', Note)


class HoldingSimple(Common):
    ROOT_NAME = 'holdingSimple'
    copy_information = NodeListField('mods:copyInformation', CopyInformation)


class Location(Location):
    holding_simple = NodeField('mods:holdingSimple', HoldingSimple)


class HierarchicalGeographic(Common):
    ROOT_NAME = 'hierarchicalGeographic'
    continent = SF('mods:continent')
    country = SF('mods:country')
    province = SF('mods:province')
    region = SF('mods:region')
    state = SF('mods:state')
    territory = SF('mods:territory')
    county = SF('mods:county')
    city = SF('mods:city')
    city_section = SF('mods:citySection')
    island = SF('mods:island')
    extraterrestrial_area = SF('mods:extraterrestrialArea')


class Temporal(Common):
    ROOT_NAME = 'temporal'
    encoding = SF('@encoding')
    text = SF('text()')


class Topic(Common):
    ROOT_NAME = 'topic'
    authority = SF('@authority')
    text = SF('text()')


class Subject(Subject):
    label = SF('@displayLabel')
    topic_list = NodeListField('mods:topic', Topic)
    hierarchical_geographic = NodeField('mods:hierarchicalGeographic', HierarchicalGeographic)
    temporal_list = NodeListField('mods:temporal', Temporal)


class RecordIdentifier(Common):
    ROOT_NAME = 'recordIdentifier'
    source = SF('@source')
    text = SF('text()')


class TargetAudience(Common):
    ROOT_NAME = 'targetAudience'
    authority = SF('@authority')
    text = SF('text()')


class BdrRecordInfo(RecordInfo):
    record_identifier_list = NodeListField('mods:recordIdentifier', RecordIdentifier)


class BdrRole(Role):
    authority_uri = xmlmap.StringField('mods:roleTerm/@authorityURI')
    value_uri = xmlmap.StringField('mods:roleTerm/@valueURI')


class BdrName(Name):
    roles = xmlmap.NodeListField('mods:role', BdrRole)


class Mods(MODSv34):
    """Map mods fields - just where we override MODSv34
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    MODSv34.ROOT_NAMESPACES['xlink'] = XLINK_NAMESPACE
    MODSv34.ROOT_NAMESPACES['xsi'] = XSI_NAMESPACE
    xsi_schema_location = SF('@xsi:schemaLocation')

    #deprecated - should use title_info_list from eulxml instead
    title_info = NodeListField('mods:titleInfo', TitleInfo)
    #override eulxml origin_info, because we add a displayLabel
    origin_info = NodeField('mods:originInfo', OriginInfo)
    #Add a commonly used related item
    collection = NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)
    #override eulxml subjects so we can add hierarchical_geographic to subject
    subjects = NodeListField('mods:subject', Subject)
    physical_description = NodeField('mods:physicalDescription', PhysicalDescription)
    locations = NodeListField('mods:location', Location)
    target_audiences = NodeListField('mods:targetAudience', TargetAudience)
    record_info_list = NodeListField('mods:recordInfo', BdrRecordInfo)
    names = xmlmap.NodeListField('mods:name', BdrName)


class ModsIndexer(object):

    DATE_NAMES = ['dateCreated', 'dateIssued', 'dateCaptured', 'dateValid', 'dateModified', 'copyrightDate', 'dateOther']
    DATE_QUALIFIERS = ['approximate', 'inferred', 'questionable']

    def __init__(self, mods_obj):
        self.mods = mods_obj

    def has_invalid_date(self):
        for d in ModsIndexer.DATE_NAMES:
            for date in self._get_dates(d):
                if not self._get_solr_date(date.text.strip()):
                    return True
        return False

    def index_data(self):
        '''Generate dict of field:data pairs for sending to solr'''
        #(xpath to data we're looking for, solr field name, single or multi-valued)
        mapping_info = [
            ('mods:physicalDescription/mods:extent', 'mods_physicalDescription_extent_ssim', 'm'),
            ('mods:physicalDescription/mods:digitalOrigin', 'mods_physicalDescription_digitalOrigin_ssim', 'm'),
            ('mods:titleInfo[@type="alternative"]/mods:title', 'mods_title_alt', 'm'),
            ('mods:subject/mods:name/mods:namePart[not(@type)]', 'subject', 'm'),
            ('mods:subject/mods:name/mods:role/mods:roleTerm[@type="text"]', 'subject', 'm'),
            ('mods:subject/mods:titleInfo/mods:title', 'mods_subject_title_ssim', 'm'),
            ('mods:subject/mods:titleInfo/mods:title', 'other_title', 'm'),
            ('mods:subject/mods:titleInfo/mods:title', 'subject', 'm'),
            ('mods:subject/mods:cartographics', 'subject', 'm'),
            ('mods:subject/mods:cartographics', 'mods_cartographics_ssim', 'm'),
            ('mods:subject/mods:geographic', 'subject', 'm'),
            ('mods:subject/mods:geographic', 'mods_geographic_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:continent', 'mods_hierarchical_geographic_continent_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:country', 'mods_hierarchical_geographic_country_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:region', 'mods_hierarchical_geographic_region_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:province', 'mods_hierarchical_geographic_province_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:state', 'mods_hierarchical_geographic_state_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:territory', 'mods_hierarchical_geographic_territory_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:county', 'mods_hierarchical_geographic_county_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:city', 'mods_hierarchical_geographic_city_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:citySection', 'mods_hierarchical_geographic_city_section_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:island', 'mods_hierarchical_geographic_island_ssim', 'm'),
            ('mods:subject/mods:hierarchicalGeographic/mods:area', 'mods_hierarchical_geographic_area_ssim', 'm'),
            ('mods:tableOfContents', 'mods_table_of_contents_ssim', 'm'),
            ('mods:typeOfResource', 'mods_type_of_resource', 'm'),
            ('mods:abstract', 'abstract', 'm'),
            ('mods:abstract', 'mods_abstract_ssim', 'm'),
            ('mods:originInfo/mods:publisher', 'publisher', 'm'),
            ('mods:originInfo/mods:publisher', 'mods_publisher_ssim', 'm'),
            ('mods:originInfo/mods:place/mods:placeTerm[@type="text"]', 'publication_place', 'm'),
            ('mods:originInfo/mods:place/mods:placeTerm[@type="text"]', 'mods_publication_place_ssim', 'm'),
            ('mods:originInfo/mods:place/mods:placeTerm[@type="code"]', 'publication_code', 'm'),
            ('mods:originInfo/mods:place/mods:placeTerm[@type="code"]', 'mods_publication_code_ssim', 'm'),
            ('mods:identifier[@type="doi"]', 'mods_id_doi_ssi', 's'),
            ('mods:identifier[@type="METSID"]', 'mets_id', 's'),
            ('mods:identifier[@type="METSID"]', 'mods_id_mets_ssi', 's'),
            ('mods:relatedItem[@type="host" and starts-with(@displayLabel,"Collection")]/mods:identifier[@type = "COLID"]', 'mods_collection_id', 'm')]
        data = {}
        for mapper in mapping_info:
            element_list = self.mods.node.xpath(mapper[0], namespaces=self.mods.ROOT_NAMESPACES)
            if element_list:
                if mapper[2] == 'm':
                    data = self._add_or_extend(data, mapper[1], [element.text for element in element_list])
                else:
                    if element_list[0].text:
                        data[mapper[1]] = element_list[0].text
        #handle dates
        for d in ModsIndexer.DATE_NAMES:
            data = self._process_date(data, d)
        #handle physicalDescription
        if self.mods.physical_description:
            for form in self.mods.physical_description.forms:
                if form.text:
                    if form.type:
                        data = self._add_or_extend(data, 'mods_physicalDescription_form_%s_ssim' % self._slugify(form.type), [form.text])
                    else:
                        data = self._add_or_extend(data, 'mods_physicalDescription_form_ssim', [form.text])
        #handle titles
        primary_titles = [title_info for title_info in self.mods.title_info_list if title_info.type != 'alternative']
        if primary_titles:
            data['primary_title'] = self.as_one_line(primary_titles[0].title)
            #this is the only place we're setting subtitle, partnumber, partname, & nonsort
            if primary_titles[0].subtitle:
                data['subtitle'] = primary_titles[0].subtitle
            if primary_titles[0].part_number:
                data['partnumber'] = primary_titles[0].part_number
            if primary_titles[0].part_name:
                data['partname'] = primary_titles[0].part_name
            if primary_titles[0].non_sort:
                data['nonsort'] = primary_titles[0].non_sort
            #rest of primary_titles go into other_titles field
            if len(primary_titles) > 1:
                other_titles = [title_info.title for title_info in primary_titles[1:]]
                data = self._add_or_extend(data, 'other_title', other_titles)
        #handle subject (topics & temporal)
        subject_elements = [subject for subject in self.mods.subjects if (subject.topic_list or subject.temporal_list)]
        for subject in subject_elements:
            #add display label to text for general subjects field
            subj_label = u''
            if subject.label:
                final_char = subject.label.strip()[-1:]
                if final_char in [u':', u'?', u'!']:
                    subj_label = u'%s ' % subject.label
                else:
                    subj_label = u'%s: ' % subject.label
            subj_text_list = [topic.text for topic in subject.topic_list]
            subj_text_list.extend([temporal.text for temporal in subject.temporal_list])
            #add all subjects to the keyword & mods_subject_ssim fields
            data = self._add_or_extend(data, 'keyword', [u'%s%s' % (subj_label, subj_text) for subj_text in subj_text_list])
            data = self._add_or_extend(data, 'mods_subject_ssim', [u'%s%s' % (subj_label, subj_text) for subj_text in subj_text_list])
            if subject.authority:
                data = self._add_or_extend(data, 'mods_subject_%s_ssim' % self._slugify(subject.authority), [u'%s%s' % (subj_label, subj_text) for subj_text in subj_text_list])
            if subject.label:
                data = self._add_or_extend(data, 'mods_subject_%s_ssim' % self._slugify(subject.label), [u'%s' % subj_text for subj_text in subj_text_list])
        #handle notes
        for note in self.mods.notes:
            #add display label to text for note field
            if note.label:
                final_char = note.label.strip()[-1:]
                if final_char in [u':', u'?', u'!']:
                    note_text = u'%s %s' % (note.label, note.text)
                else:
                    note_text = u'%s: %s' % (note.label, note.text)
            else:
                note_text = note.text
            #add all notes to the note field
            data = self._add_or_extend(data, 'note', [note_text])
            if note.type:
                data = self._add_or_extend(data, 'mods_note_%s_ssim' % self._slugify(note.type), [note.text])
            if note.label:
                data = self._add_or_extend(data, 'mods_note_%s_ssim' % self._slugify(note.label), [note.text])
        #GENRES
        for genre in self.mods.genres:
            if genre.text:
                data = self._add_or_extend(data, 'genre', [genre.text])
                if genre.authority:
                    genre_field_name = u'mods_genre_%s_ssim' % self._slugify(genre.authority)
                    data = self._add_or_extend(data, genre_field_name, [genre.text])
        #mods_id
        if self.mods.id:
            data['mods_id'] = self.mods.id
        #record info
        for record_info in self.mods.record_info_list:
            for record_id in record_info.record_identifier_list:
                #add all record_identifiers
                field_name = 'mods_record_info_record_identifier_ssim'
                data = self._add_or_extend(data, field_name, [record_id.text])
                #add a field with the source specified as well, if present
                if record_id.source:
                    field_name = 'mods_record_info_record_identifier_%s_ssim' % self._slugify(record_id.source)
                    data = self._add_or_extend(data, field_name, [record_id.text])
        #related items - easier to handle with xpath for now
        related_item_els = self.mods.node.xpath('mods:relatedItem', namespaces=self.mods.ROOT_NAMESPACES)
        for related_item in related_item_els:
            type = related_item.get('type')
            label = related_item.get('displayLabel')
            title_els = related_item.xpath('mods:titleInfo/mods:title', namespaces=self.mods.ROOT_NAMESPACES)
            titles = [title.text for title in title_els]
            if type == 'host' and label and label.startswith('Collection'):
                if 'collection_title' in data:
                    data['collection_title'].extend(titles)
                else:
                    data['collection_title'] = titles
            #any relatedItem titles that aren't collection titles go into other_title
            else:
                if 'other_title' in data:
                    data['other_title'].extend(titles)
                else:
                    data['other_title'] = titles
            #solrize ids here as well
            identifier_els = related_item.xpath('mods:identifier', namespaces=self.mods.ROOT_NAMESPACES)
            for identifier in identifier_els:
                if identifier.text:
                    type = identifier.get('type')
                    if type:
                        data = self._add_or_extend(data, 'mods_related_id_%s_ssim' % self._slugify(type), [identifier.text])
                    else:
                        data = self._add_or_extend(data, 'mods_related_id_ssim', [identifier.text])
            name_els = related_item.xpath('mods:name', namespaces=self.mods.ROOT_NAMESPACES)
            for name in name_els:
                name_parts = name.xpath('mods:namePart', namespaces=self.mods.ROOT_NAMESPACES)
                for np in name_parts:
                    data = self._add_or_extend(data, 'mods_related_name_ssim', [np.text])
        #access conditions
        access_condition_els = self.mods.node.xpath('mods:accessCondition', namespaces=self.mods.ROOT_NAMESPACES)
        if access_condition_els:
            for access_condition in access_condition_els:
                type = access_condition.get('type')
                href = access_condition.get('href') #should really be xlink:href
                if type == 'use and reproduction':
                    data = self._add_or_extend(data, 'mods_access_condition_use_text_tsim', [access_condition.text])
                    if href:
                        data = self._add_or_extend(data, 'mods_access_condition_use_link_ssim', [href])
                elif type == 'logo':
                    if href:
                        data = self._add_or_extend(data, 'mods_access_condition_logo_ssim', [href])
        #other id's not handled above
        identifier_els = [idt for idt in self.mods.identifiers if idt.type not in ['COLID', 'URI', 'doi', 'METSID']]
        for identifier in identifier_els:
            if identifier.text:
                data = self._add_or_extend(data, 'identifier', [identifier.text])
                if identifier.label:
                    data = self._add_or_extend(data, 'mods_id_%s_ssim' % self._slugify(identifier.label), [identifier.text])
                if identifier.type:
                    data = self._add_or_extend(data, 'mods_id_%s_ssim' % self._slugify(identifier.type), [identifier.text])
        #names
        try:
            for name in self.mods.names:
                nameparts = [np.text for np in name.name_parts if not np.type]
                roles = [role.text for role in name.roles if role.type != 'code']
                dates = [np.text for np in name.name_parts if np.type == 'date']
                if nameparts and nameparts[0]:
                    data = self._add_or_extend(data, 'name', [nameparts[0]])
                    if dates and dates[0]:
                        date = u', %s' % dates[0]
                    else:
                        date = u''
                    if roles and roles[0]:
                        data = self._add_or_extend(data, 'contributor_display', ['%s%s (%s)' % (nameparts[0], date, roles[0])])
                        data = self._add_or_extend(data, 'mods_role_ssim', [roles[0]])
                        data = self._add_or_extend(data, 'mods_role_%s_ssim' % self._slugify(roles[0]), [nameparts[0]])
                        if roles[0].endswith(u' place'):
                            data = self._add_or_extend(data, 'mods_name_place_ssim', [nameparts[0]])
                        else:
                            data = self._add_or_extend(data, 'mods_name_nonplace_ssim', [nameparts[0]])
                        if roles[0] == 'creator':
                            data = self._add_or_extend(data, 'creator', [nameparts[0]])
                        else:
                            data = self._add_or_extend(data, 'contributor', [nameparts[0]])
                    else:
                        data = self._add_or_extend(data, 'mods_name_nonplace_ssim', [nameparts[0]])
                        data = self._add_or_extend(data, 'contributor_display', ['%s%s' % (nameparts[0], date)])
        except Exception as e:
            raise Exception(u'names: %s' % repr(e))

        return data

    def as_one_line(self, text):
        return u' '.join([t.strip() for t in text.splitlines()])

    def _add_or_extend(self, data, field_name, data_list):
        data_list = [d for d in data_list if d]
        if data_list:
            if field_name in data:
                data[field_name].extend(data_list)
            else:
                data[field_name] = data_list
        return data

    def _slugify(self, text):
        #very similar functionality to django's slugify function
        text = text.strip().lower().replace(u' ', u'_')
        #we can return str instead of unicode because we're generating a slug, not working with data
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        pattern = re.compile('\W')
        text = pattern.sub('', text)
        return text

    def _get_solr_date(self, date):
        if re.match('^\d{4}-\d{2}-\d{2}$', date):
            date = date + 'T00:00:00Z'
        elif re.match('^\d{4}-\d{2}$', date):
            date = date + '-01T00:00:00Z'
        elif re.match('^\d{4}$', date):
            date = date + '-01-01T00:00:00Z'
        else:
            date = None
        return date

    def _get_dates(self, date_name):
        #get all the dates, excluding any empty dates
        date_xpath = 'mods:originInfo/mods:%s' % date_name
        dates_els = self.mods.node.xpath(date_xpath, namespaces=self.mods.ROOT_NAMESPACES)
        return [d for d in dates_els if d.text]


    def _process_date(self, data, date_name):
        #dates - actual date fields are single value, but we put other dates into a multi-value string fields
        try:
            for date in self._get_dates(date_name):
                #see if we can get a valid date value to put in solr date field
                solr_date = self._get_solr_date(date.text.strip())
                qualifier = date.get('qualifier')
                point = date.get('point')
                key_date = date.get('keyDate')
                #these are the main valid dates (ignore questionable and end dates here)
                if solr_date and (date_name not in data) and (qualifier != 'questionable') and (point != 'end' or key_date == 'yes'):
                    #for all valid dates, add the year to the year field (eg. dateCreated_year_ssim)
                    data = self._add_or_extend(data, '%s_year_ssim' % date_name, [solr_date[:4]])
                    data[date_name] = solr_date
                #any other dates get put in generic field (eg. dateCreated_ssim)
                else:
                    data = self._add_or_extend(data, '%s_ssim' % date_name, [date.text])
                #some special facets handling for dateOther
                if date_name == 'dateOther':
                    type = date.get('type')
                    if type == 'quarterSort':
                        data = self._add_or_extend(data, 'mods_dateOther_quarter_facet', [date.text])
                    elif type == 'yearSort':
                        data = self._add_or_extend(data, 'mods_dateOther_year_facet', [date.text])
                #index dates with qualifiers or end dates in special fields
                if point == 'end':
                    data = self._add_or_extend(data, 'mods_%s_end_ssim' % date_name, [date.text])
                if qualifier in ModsIndexer.DATE_QUALIFIERS:
                    data = self._add_or_extend(data, 'mods_%s_%s_ssim' % (date_name, qualifier), [date.text])
        except Exception as e:
            raise Exception(u'%s: %s' % (date_name, repr(e)))
        return data


def make_mods():
    """Helper that returns Mods object."""
    m = Mods()
    m.xsi_schema_location = XSI_LOCATION
    return m

