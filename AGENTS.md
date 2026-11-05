# AGENTS.md — Repository Agent Instructions

These instructions apply to this Python library. This file is the source of truth for repository coding guidance; if other local instruction files conflict, follow this one. Keep it under 300 lines, preserving useful shared conventions and the project index.

- [Project basics](#project-basics)
- [Coding and testing](#coding-and-testing)
- [Workflow and privacy](#workflow-and-privacy)
- [Commit messages](#commit-messages)
- [Project index](#project-index)

## Project basics

- The project root is the directory containing this file and `pyproject.toml`. Assume commands run from that directory.
- Follow `pyproject.toml` for Python and dependency requirements. Run scripts through `uv run`, rather than invoking Python directly.
- Install local tooling with `uv sync --locked --group local`; run the suite with `uv run ./run_tests.py`.
- Build both package formats with `uv build`. Keep every bundled XSD in both the wheel and source archive.
- Keep compatible dependency ranges in `pyproject.toml` and exact development versions in `uv.lock`. Use `uv_build` as the build backend.

## Coding and testing

- Keep changes focused. Preserve public XML classes, field names, namespaces, and serialization unless a change is specifically requested.
- Use Python type hints in new code. Prefer builtin generics and `str | None`; check for missing XML nodes explicitly.
- Keep helpers small and at module scope. Prefer explicit control flow and a single return when that remains clear.
- For new runnable scripts, put argument handling and calls to helpers in `main() -> None`, invoked under `if __name__ == '__main__':`.
- Write present-tense docstrings with triple quotes on their own lines. Begin test docstrings with `Checks...`. For internal helpers, end with `Called by: ...` naming actual callers; describe the intended use of public library functions without inventing an in-repository caller.
- Use `unittest`, including an expected case and an error case for new behavior. Tests use local XML and bundled schemas.
- Check changed Python with Pylance or Pyright in basic mode, using `.venv` and the local `typings/` definitions. Fix errors without suppressing diagnostics.
- The type definitions describe fields installed dynamically by neuxml. Keep them aligned with the installed library and the Darwin Core field declarations.
- Follow `ruff.toml`. Avoid unrelated formatting changes in legacy files.
- Let Markdown paragraphs wrap naturally. Keep the table of contents aligned with the document's sections.

## Workflow and privacy

- Read the surrounding code before editing and preserve the user's manual changes. Work directly from the authorized request; an issue or formal plan is not a prerequisite for local changes.
- Work on the requested branch. Create or amend commits only when the user explicitly requests it. Otherwise, finish the authorized local work and leave it uncommitted for review.
- Posting to GitHub, pushing, publishing, merging pull requests, and closing issues require their own authorization. Do not arrange automatic issue closure through commit messages or pull-request descriptions unless requested.
- For code changes, update relevant tests and run `uv run ./run_tests.py`. For dependency or packaging changes, update `uv.lock`, verify locked syncing, and test the installed package outside the source checkout.
- Report the files changed, checks actually run, and any remaining work. Distinguish local, committed, and pushed changes. If a check cannot run, explain what failed and give a concrete next step.
- Keep private operational information and security findings out of tracked files and repository posts. Never include full local or server filesystem paths in documentation.
- Review the exact outgoing text for private information before an authorized repository post. Identify Codex as the author of GitHub posts or edits, and distinguish the user's words from the agent's summary.
- Keep documentation focused on local usage, tests, and packaging. Server deployment instructions do not belong in this library's README.

## Commit messages

- Apply these conventions only after the user authorizes the commit. A suggested message or approval of the implementation does not authorize committing.
- Group related files into logical, focused commits; a separate commit for every file is not required.
- Keep each commit message to no more than ten words.
- Use present tense to complete the phrase "This commit..." Begin with a fitting verb such as "Adds," "Implements," or "Updates."

## Project index

- `bdrxml/mods.py` extends neuxml's MODS mappings. `make_mods()` defaults to MODS 3.8; callers can explicitly request 3.7.
- `bdrxml/darwincore.py` builds fields from `DWC_TERMS` and validates against local schemas.
- `bdrxml/foxml.py`, `mets.py`, `irMetadata.py`, `rels.py`, and `rights.py` describe the other BDR XML formats.
- `bdrxml/schemas/` contains the local validation schemas. The uv build backend includes these files with the Python module; verify they remain in both package formats.
- `test/` contains synthetic XML, sample documents, and unit tests. `run_tests.py` collects the suite.
