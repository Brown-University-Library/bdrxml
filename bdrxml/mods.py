from eulxml.xmlmap import mods as eulmods
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeListField, NodeField
#some imports here because users need to instantiate these classes to use Mods
from eulxml.xmlmap.mods import MODS_NAMESPACE
from eulxml.xmlmap.mods import DateCreated, DateIssued, DateCaptured, DateValid, DateModified, CopyrightDate, DateOther
from eulxml.xmlmap.mods import RecordInfo, Note, Identifier, AccessCondition, NamePart, Role, Name, Genre
from eulxml.xmlmap.mods import Language, LanguageTerm, Location, TitleInfo, Abstract, PhysicalDescription
from eulxml.xmlmap.mods import Part, PartDetail, PartExtent, RelatedItem


class OriginInfo(eulmods.OriginInfo):
    label = SF('@displayLabel')


class Collection(eulmods.RelatedItem):
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')


class HierarchicalGeographic(eulmods.Common):
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


class Subject(eulmods.Subject):
    hierarchical_geographic = NodeField('mods:hierarchicalGeographic', HierarchicalGeographic)


class Mods(eulmods.MODSv34):
    """Map mods fields - just where we override eulmods.MODSv34
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


def make_mods():
    """Helper that returns Mods object."""
    m = Mods()
    return m

