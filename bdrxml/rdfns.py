'''
From https://github.com/emory-libraries/eulfedora; Apache 2.0 license
'''
from rdflib.namespace import ClosedNamespace

# ids copied from http://www.fedora.info/definitions/1/0/fedora-relsext-ontology.rdfs
fedora_rels = [ 
    'fedoraRelationship',
    'isPartOf',
    'hasPart',
    'isConstituentOf',
    'hasConstituent',
    'isMemberOf',
    'hasMember',
    'isSubsetOf',
    'hasSubset',
    'isMemberOfCollection',
    'hasCollectionMember',
    'isDerivationOf',
    'hasDerivation',
    'isDependentOf',
    'hasDependent',
    'isDescriptionOf',
    'HasDescription',
    'isMetadataFor',
    'HasMetadata',
    'isAnnotationOf',
    'HasAnnotation',
    'hasEquivalent',
]


relsext = ClosedNamespace('info:fedora/fedora-system:def/relations-external#',
                          fedora_rels)
''':class:`rdflib.namespace.ClosedNamespace` for the `Fedora external
relations ontology
<http://www.fedora.info/definitions/1/0/fedora-relsext-ontology.rdfs>`_.
'''

model = ClosedNamespace('info:fedora/fedora-system:def/model#', [
    'hasModel',
])
''':class:`rdflib.namespace.ClosedNamespace` for the Fedora model
namespace (currently only includes ``hasModel``).'''
