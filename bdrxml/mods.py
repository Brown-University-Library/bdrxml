from eulxml.xmlmap import mods as eulmods
from eulxml.xmlmap import StringField as SF

MODS_NAMESPACE = eulmods.MODS_NAMESPACE

class Mods(eulmods.MODSv34):
    """Map mods fields.
    
    Fields documented at:
    http://www.loc.gov/standards/mods/mods-outline.html
    """
    id = SF('@ID')

def make_mods():
    """
    Helper that sets the XSD and returns Mods object.
    """
    m = Mods()
    return m
