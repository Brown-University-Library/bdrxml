bdrxml
======
[![Tests Status](https://github.com/Brown-University-Library/bdrxml/workflows/CI%20tests/badge.svg)](https://github.com/Brown-University-Library/bdrxml/actions)

## Brief overview

bdrxml reads and writes XML metadata for the Brown Digital Repository, including MODS, METS, FOXML, Darwin Core, relationships, and rights metadata.

## More info

- [Brief overview](#brief-overview)
- [More info](#more-info)
- [Local installation](#local-installation)
- [Usage](#usage)
- [Tests and packaging](#tests-and-packaging)
- [Primary dependencies](#primary-dependencies)

Version 2.0 uses Princeton's published [neuxml package](https://pypi.org/project/neuxml/) for XML mapping. Applications keep importing BDR-specific classes from `bdrxml`; direct imports from `eulxml` should change to `neuxml`. Python requirements and package metadata live in `pyproject.toml`, and `uv.lock` records exact development versions.

## Local installation

Starting in the directory where you keep local checkouts, run these commands with Git and uv 0.13.6 or newer available:

```sh
mkdir bdrxml_stuff
cd bdrxml_stuff
git clone https://github.com/Brown-University-Library/bdrxml.git
cd bdrxml
uv sync --locked --group local
```

uv selects Python from `pyproject.toml`. The local group includes XML type definitions for editor checks. The runtime and test groups use the library's declared dependencies and Python's built-in `unittest`.

## Usage

```python
from bdrxml import mods
from neuxml.xmlmap import load_xmlobject_from_string

record = mods.make_mods()
record.title = 'Example title'
xml = record.serialize()
loaded = load_xmlobject_from_string(xml, mods.Mods)
```

`make_mods()` creates MODS 3.8 by default. Use `make_mods(schema_version='3.7')` when an application requires the earlier schema. BDR-specific MODS validation uses bundled schema files.

## Tests and packaging

From the repository root:

```sh
uv run ./run_tests.py
uv build
```

The tests read local XML and do not require a BDR service. `uv build` uses uv's own `uv_build` backend to create a wheel and source archive in `dist/`, including the schema files. The source archive also includes the tests and local tooling configuration. CI checks installation and tests with the locked dependencies.

## Primary dependencies

- **neuxml:** supplies the XML mapping classes used throughout `bdrxml/`.
- **lxml:** parses XML and validates bundled schemas in `bdrxml/darwincore.py`; neuxml also uses it.
- **rdflib:** supplies RDF namespace definitions in `bdrxml/rdfns.py` and supports neuxml's RDF mappings.
- **PLY:** parses XPath expressions inside neuxml. The minimum version keeps its generated parser tables compatible with current Python.
- **types-lxml:** local editor tooling only. **uv_build:** package build tooling only.

The inventory follows the former package declarations, current imports, and `uv.lock`. No separate server dependency set is needed for this library.
