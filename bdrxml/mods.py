from eulxml.xmlmap import mods as eulmods
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeListField, NodeField

MODS_NAMESPACE = eulmods.MODS_NAMESPACE


class TitleInfo(eulmods.TitleInfo):
    label  = SF('@displayLabel')


class DateOther(eulmods.Date):
    ROOT_NAME = 'dateOther'
    type = SF('@type')


class OriginInfo(eulmods.OriginInfo):
    other = NodeListField('mods:dateOther', DateOther,
        verbose_name='Date Other',
        help_text='Other Date')

class Collection(eulmods.RelatedItem):
    name = SF('mods:titleInfo/mods:title')
    id = SF('mods:identifier[@type="COLID"]')


class Mods(eulmods.MODSv34):
    """Map mods fields.
    
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    id = SF('@ID')
    #override eulxml title_info, because we need to support multiple titles
    title_info = NodeListField('mods:titleInfo', TitleInfo)
    #override eulxml origin_info, because we need to support dateOther
    origin_info = NodeField('mods:originInfo', OriginInfo)
    #Add a commonly used related item
    collection = NodeField('mods:relatedItem[@displayLabel="Collection"]', Collection)


def make_mods():
    """
    Helper that sets the XSD and returns Mods object.
    """
    m = Mods()
    return m
