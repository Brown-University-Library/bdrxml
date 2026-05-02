bdrxml
======
[![Tests Status](https://github.com/Brown-University-Library/bdrxml/workflows/CI%20tests/badge.svg)](https://github.com/Brown-University-Library/bdrxml/actions)

Reading and writing XML for the Fedora-based BDR.

Overview
--------

`bdrxml` is a small shared Python package for creating, parsing, and inspecting
XML structures used across Brown Digital Repository projects. It provides
`eulxml.xmlmap` object mappings and helper builders for MODS, Simple Darwin
Core, BDR METS, BDR and Hydra rights metadata, IR/deposit metadata, Fedora
FOXML, RELS-EXT, and RELS-INT. It is a library, not a web application or
service process; downstream BDR apps import it for metadata construction,
validation, packaging, rights handling, indexing support, and Fedora-era
relationship data.

Installation
------------

For local development, install the virtualenv in the outer directory that
contains this repository, then point an `env` symlink at it. For example, from
an outer directory shaped like this:

```text
bdrxml_stuff/
  bdrxml/
  env -> ./venv_bdrxml_02
  venv_bdrxml_02/
```

create and populate the environment with `uv`:

```bash
cd /path/to/bdrxml_stuff
uv venv --python 3.8 venv_bdrxml_02
ln -sfn ./venv_bdrxml_02 env

cd bdrxml
source ../env/bin/activate
uv pip sync ./requirements.txt
uv pip install setuptools
```

re the simlink:
- -s: create a symbolic link
- -f: force replacement if the destination already exists
- -n: if the destination is an existing symlink to a directory, treat the symlink itself as the thing to replace, not the directory it points to

`setuptools` is needed because `eulxml==1.1.3` imports `pkg_resources`, but
modern `uv` virtualenvs do not include `setuptools` by default.

Run tests from the `bdrxml` repo directory:

```bash
source ../env/bin/activate
python run_tests.py
```
