import re
import unicodedata
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeListField, NodeField
#import everything from eulxml.xmlmap.mods because clients have to use a lot of
#   those classes, and we're just overriding a few of them here.
from eulxml.xmlmap.mods import *


class OriginInfo(OriginInfo):
    label = SF('@displayLabel')


class Collection(RelatedItem):
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')


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


class Subject(Subject):
    hierarchical_geographic = NodeField('mods:hierarchicalGeographic', HierarchicalGeographic)


class Mods(MODSv34):
    """Map mods fields - just where we override MODSv34
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    #deprecated - should use title_info_list from eulxml instead
    title_info = NodeListField('mods:titleInfo', TitleInfo)
    #override eulxml origin_info, because we add a displayLabel
    origin_info = NodeField('mods:originInfo', OriginInfo)
    #Add a commonly used related item
    collection = NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)
    #override eulxml subjects so we can add hierarchical_geographic to subject
    subjects = NodeListField('mods:subject', Subject)

    def index_data(self):
        '''Generate dict of field:data pairs for sending to solr
        TODO: consider refactoring into a different class'''
        #(xpath to data we're looking for, solr field name, single or multi-valued)
        mapping_info = [
            ('mods:titleInfo[@type="alternative"]/mods:title', 'mods_title_alt', 'm'),
            ('mods:genre[@authority="bdr"]', 'genre_bdr', 'm'),
            ('mods:genre[@authority="aat"]', 'genre_aat', 'm'),
            ('mods:genre[@authority="local"]', 'genre_local', 'm'),
            ('mods:subject/mods:titleInfo/mods:title', 'other_title', 'm'),
            ('mods:subject/mods:name/mods:namePart[not(@type)]', 'subject', 'm'),
            ('mods:subject/mods:name/mods:role/mods:roleTerm[@type="text"]', 'subject', 'm'),
            ('mods:subject/mods:titleInfo/mods:title', 'subject', 'm'),
            ('mods:subject/mods:cartographics', 'subject', 'm'),
            ('mods:subject/mods:geographic', 'subject', 'm'),
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
            ('mods:subject/mods:topic', 'keyword', 'm'),
            ('mods:tableOfContents', 'other_title', 'm'),
            ('mods:typeOfResource', 'mods_type_of_resource', 'm'),
            ('mods:abstract', 'abstract', 'm'),
            ('mods:originInfo/mods:publisher', 'publisher', 'm'),
            ('mods:originInfo/mods:place/mods:placeTerm[@type="text"]', 'publication_place', 'm'),
            ('mods:originInfo/mods:place/mods:placeTerm[@type="code"]', 'publication_code', 'm'),
            ('mods:identifier[@type="doi"]', 'mods_id_doi_ssi', 's'),
            ('mods:identifier[@type="METSID"]', 'mets_id', 's'),
            ('mods:relatedItem[@type="host" and starts-with(@displayLabel,"Collection")]/mods:identifier[@type = "COLID"]', 'mods_collection_id', 'm')]
        data = {}
        for mapper in mapping_info:
            element_list = self.node.xpath(mapper[0], namespaces=self.ROOT_NAMESPACES)
            if element_list:
                if mapper[2] == 'm':
                    data = self._add_or_extend(data, mapper[1], [element.text for element in element_list])
                else:
                    data[mapper[1]] = element_list[0].text
        #handle dates
        data = self._process_date(data, 'dateCreated')
        data = self._process_date(data, 'dateIssued')
        data = self._process_date(data, 'dateCaptured')
        data = self._process_date(data, 'dateValid')
        data = self._process_date(data, 'dateModified')
        data = self._process_date(data, 'copyrightDate')
        data = self._process_date(data, 'dateOther')
        #handle titles
        primary_titles = [title_info for title_info in self.title_info_list if title_info.type != 'alternative']
        if primary_titles:
            data['primary_title'] = primary_titles[0].title
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
        #handle notes
        for note in self.notes:
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
            else:
                if note.label:
                    data = self._add_or_extend(data, 'mods_note_%s_ssim' % self._slugify(note.label), [note.text])
        #mods_id
        if self.id:
            data['mods_id'] = self.id
        #related items - easier to handle with xpath for now
        related_item_els = self.node.xpath('mods:relatedItem', namespaces=self.ROOT_NAMESPACES)
        for related_item in related_item_els:
            type = related_item.get('type')
            label = related_item.get('displayLabel')
            title_els = related_item.xpath('mods:titleInfo/mods:title', namespaces=self.ROOT_NAMESPACES)
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
        #access conditions
        access_condition_els = self.node.xpath('mods:accessCondition', namespaces=self.ROOT_NAMESPACES)
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
        identifier_els = self.node.xpath('mods:identifier[@type and not(@type="COLID") and not(@type="URI") and not(@type="doi") and not(@type="METSID")]', namespaces=self.ROOT_NAMESPACES)
        for identifier in identifier_els:
            type = identifier.get('type')
            if type:
                data = self._add_or_extend(data, 'mods_id_%s_ssim' % type, [identifier.text])
            else:
                data = self._add_or_extend(data, 'identifier', [identifier.text])
        #names
        try:
            for name in self.names:
                nameparts = [np.text for np in name.name_parts if not np.type]
                roles = [role.text for role in name.roles if role.type == 'text']
                if nameparts and nameparts[0]:
                    data = self._add_or_extend(data, 'name', [nameparts[0]])
                    if roles and roles[0]:
                        data = self._add_or_extend(data, 'contributor_display', ['%s (%s)' % (nameparts[0], roles[0])])
                        if roles[0] == 'creator':
                            data = self._add_or_extend(data, 'creator', [nameparts[0]])
                        else:
                            data = self._add_or_extend(data, 'contributor', [nameparts[0]])
                    else:
                        data = self._add_or_extend(data, 'contributor_display', ['%s' % nameparts[0]])
        except Exception as e:
            raise Exception(u'names: %s' % repr(e))

        return data

    def _add_or_extend(self, data, field_name, data_list):
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

    def _process_date(self, data, date_name):
        #dates - actual date fields are single value, but we put other dates into a multi-value string fields
        try:
            #for now, we'll ignore dates marked as questionable and end dates
            date_xpath = 'mods:originInfo/mods:%s[not(@qualifier="questionable") and (not(@point) or @point!="end" or @keyDate="yes")]' % date_name
            dates_els = self.node.xpath(date_xpath, namespaces=self.ROOT_NAMESPACES)
            if dates_els:
                for date in dates_els:
                    #make sure it's not an empty date element
                    if date.text:
                        if date_name not in data:
                            #see if we can get a valid date value to put in solr
                            solr_date = self._get_solr_date(date.text.strip())
                            if solr_date:
                                data[date_name] = solr_date
                            else:
                                data = self._add_or_extend(data, '%s_ssim' % date_name, [date.text])
                        else:
                            #handle remaining dates
                            data = self._add_or_extend(data, '%s_ssim' % date_name, [date.text])
                        #some special facets handling for dateOther
                        if date_name == 'dateOther':
                            type = date.get('type')
                            if type == 'quarterSort':
                                data = self._add_or_extend(data, 'mods_dateOther_quarter_facet', [date.text])
                            elif type == 'yearSort':
                                data = self._add_or_extend(data, 'mods_dateOther_year_facet', [date.text])
        except Exception as e:
            raise Exception(u'%s: %s' % (date_name, repr(e)))
        return data


def make_mods():
    """Helper that returns Mods object."""
    m = Mods()
    return m

