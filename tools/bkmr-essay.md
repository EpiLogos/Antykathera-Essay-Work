# `bkmr-essay` Retrieval Shim

The shim keeps `bkmr` modular without allowing its thin bookmark schema to rewrite, flatten, or become authoritative over the Return of Zero vault.

```text
tools/bkmr-essay status
tools/bkmr-essay sync records --dry-run
tools/bkmr-essay sync passages
tools/bkmr-essay search passages "vimarsa" --limit 8
tools/bkmr-essay search records "Kaplan zero" --limit 5
tools/bkmr-essay query arguments "reflexive awareness" --semantic-provider gemini --limit 5
```

`sync` generates adapter files and a hash manifest under `.bkmr/`. The six independent collections are `records`, `passages`, `arguments`, `sections`, `concepts`, and `rooms`. `records` indexes the canonical one-work `SOURCE.md` houses; `passages` carries stable IDs, locators, statuses, provenance, and canonical fragments, never a second transcription. `rooms` contains the compact room and reading-route surfaces. Adapters expose stable IDs, canonical paths, status, locators, and consumer metadata; they do not import the Books pool. Canonical Markdown remains the authority. Each collection database is a disposable cache and is rebuilt deterministically on sync, avoiding a bkmr 6.5.0 duplicate-import defect; rerunning semantic sync therefore re-embeds that collection.

The default import and lexical search are local. A semantic sync or query requires an explicit provider argument. That is a deliberate privacy and copyright gate: only lawful, non-sensitive derivative metadata or authorised short excerpts may enter an adapter sent to OpenAI or Gemini. Never index the Books pool directly, and never treat a retrieval result as citation or quotation verification.
