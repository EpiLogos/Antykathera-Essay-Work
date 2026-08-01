# Sources

Every recoverable work has one canonical file at `<source_id>/SOURCE.md`. That file
contains the work's bibliographic identity, scholarly notes, quotes and excerpts,
passage metadata, essay uses, and reading material. Those functions do not create
parallel files.

Frank may add an optional `NOTES.md` beside any source. It is free-form,
agent-read-only, and excluded from generated source projections. Agents use it to
recover Frank's encounter and intent, never as quotation or citation authority.

Create a source from the canonical template, then rebuild and verify the generated locators:

```bash
python3 tools/build-source-projections.py --project-root .
python3 tools/build-source-projections.py --project-root . --check
```

Current inventory: 83 sources and
133 stable passages.
