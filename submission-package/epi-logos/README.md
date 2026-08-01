# Epi-Logos Reader Companion

Epi-Logos is the installable companion to the published Obsidian work. It reads, follows, teaches, and investigates the linked publication through one QL/MEF instrument.

The package does not depend on the work retaining its current title, section names, node counts, or curated routes. It begins from the current vault entry or the reader's present page, discovers the assets and links that actually exist, and follows the work from there.

## What ships

- **The bootstrap** (`skills/using-epi-logos`) — establishes the subject/instrument relation, the `0/1 … 5→0` movement, unified QL/MEF conduct, and claim-status discipline.
- **The reader entrance** (`skills/walk-the-essay`) — reads linearly, follows linked depth, teaches from the live page, resumes prior paths, and returns through the work.
- **Linked-vault retrieval** (`skills/okf-wiki`) — reads Obsidian-style Markdown and the shipped OKF-compatible snapshot, follows ordinary links and embeds, recovers the local argument, and keeps source and quotation use honest.
- **Pedagogy** (`skills/converse-pedagogically`) — teaches through the live question and the pages actually encountered.
- **Specialist operations** — tetralemma, CMEA, encounter-axis, topological, etymological, and other operations used internally as lenses and movements of the same QL/MEF instrument.
- **Reader traversal resources** (`resources/reader/`) — the traversal-ledger contract and a copyable Markdown note.
- **The current publication snapshot** (`resources/essay-okf/index.md`) — the entry to a generated linked reader bundle. Its present census is discovered from that index rather than encoded into the skills.
- **QL/MEF resources** (`data/`, `resources/canon/`, `resources/units/`) — the coordinate and lens material used when the reading needs formal depth.

The package runs without a session hook, external persona injection, or semantic retrieval service.

## Reader movement

The companion treats linear and non-linear reading as equally native:

- continue through a manuscript or declared sequence;
- open from prose into an idea, source, diagram, or neighbouring movement;
- follow a question transversely across the vault;
- return to an earlier page or question with a changed understanding.

When a reader wants continuity, the companion maintains a reader-owned traversal ledger using `resources/reader/TRAVERSAL-LEDGER.md`. The ledger can be kept in a copied vault, held in a companion session, or exported as Markdown. It never writes into the published essay or source pages.

## QL/MEF

QL and MEF are one instrument. QL's positional movement and MEF's lens-conditioned encounter are distinguishable operations inside a single reading. Tetralemma and the other specialist procedures are lenses within that reading, not separate systems presented to the user.

The body of an answer remains natural prose. Coordinates and lens names appear only when they clarify something the reader is actually meeting.

## Epi-Card

The adjacent `epi-card-system-v1/` package is an optional integration specification. Its contracts validate, but an Epi-Card application runtime is not included.

The intended relation is:

`published vault → reader traversal ledger → QL/MEF reading → optional Epi-Card encounter capsule`

Ordinary reading never requires the card system. At a meaningful return, a reader may eventually choose to crystallise a frozen traversal, its selected source links, achieved movement, remainder, and next ground as a portable card. The card does not become authority over the vault or the ledger.

The honest artifact inventory is `../MANIFEST.json`.

## Install

From a development checkout:

```text
/plugin marketplace add /path/to/submission-package
/plugin install epi-logos@epi-logos-submission
```

For direct local testing:

```text
claude --plugin-dir /path/to/submission-package/epi-logos
```

The marketplace manifest lists only the installable Epi-Logos plugin. The card specification remains in the submission manifest until it has a real runtime and plugin boundary.
