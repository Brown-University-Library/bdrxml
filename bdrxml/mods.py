from eulxml.xmlmap import mods as eulmods
from eulxml.xmlmap import StringField as SF
from eulxml.xmlmap import NodeListField

MODS_NAMESPACE = eulmods.MODS_NAMESPACE


class TitleInfo(eulmods.TitleInfo):
    label  = SF('@displayLabel')


class Mods(eulmods.MODSv34):
    """Map mods fields.
    
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    id = SF('@ID')
    #override eulxml title_info, because we need to support multiple titles
    title_info = NodeListField('mods:titleInfo', TitleInfo)


def make_mods():
    """
    Helper that sets the XSD and returns Mods object.
    """
    m = Mods()
    return m
