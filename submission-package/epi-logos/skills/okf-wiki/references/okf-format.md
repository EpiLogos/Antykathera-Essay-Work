# OKF reader schema

This is the portable schema used by the published essay body. Read `SKILL.md` for the traversal protocol.

## OKF core

An OKF bundle is a directory of Markdown nodes joined by ordinary Markdown links.

- `type` is required on every node.
- `index.md` is the progressive-disclosure entry and routing surface.
- `log.md` records export provenance and recency.
- links are edges; their argumentative meaning comes from the source node's prose and headings.
- `resource:` identifies a non-Markdown artifact that is not a traversable node.

The shipped essay uses these types:

| Type | Role |
|---|---|
| `section` | One of the 48 movements: thesis, development, boundary, and transition |
| `argument` and argument refinements | Major claim with warrants, tension, and opening |
| `concept` | Controlling definition, argumentative use, sources, and relations |
| `path` | Ordered reading route through the graph |
| `braid` | Transverse research route across non-adjacent movements |
| `argument-map` | Network view of claims and dependencies |
| `source-record` | Bibliographic identity, licensed use, readiness, and claim boundary |
| `quote-dossier` | Passage transcription, locator, verification, relation, and use boundary |
| `source-extraction` | Development provenance and quotation staging; never quotation authority |
| `dialogue-record` | Provenance of an idea's formation through dialogue; never evidence. The citation/quotation gate does not apply: quotations of the dialogue are quotations of the conversation, never of the named works |
| supporting document types | Included orientation, venue, method, or in-house material |
| `index` | Bundle routing map |
| `log` | Export history and source digest |

## Argument fields

- `claim_status`: `Derived`, `Argued`, `Offered`, or `Open`. Relay it as written; never launder it upward.
- `register`: `symbolon`, `matheme`, `mytheme`, `episteme`, or a declared cross-register composition (for example `matheme/mytheme`). It is the content's own anatomy, independent of node type; placement must match the operation the record performs. A record with no declared register is a register-census debt, not an opportunity to guess from folder placement.
- `coordinates`: the node's essay station/position or other canonical coordinates. `#` is the Möbius parent, not P4. P and L families remain distinct.
- `aperture`: calibrated contextual entry such as novice, expert, or prerequisite framing.
- `analogia`: nodes said in relation to one structure. This marks focal relation, not identity or proof.
- tags, aliases, dependencies, and consumer fields remain meaningful when present.

## Source fields

A `source-record` may carry independent `metadata_status`, `edition_status`, `citation_status`, and `quote_status` values. `citation_status: citation-ready` establishes a usable bibliographic identity and may license attributed paraphrase within the record's boundary. It does not license exact quotation.

A `quote-dossier` supplies passage-level authority. An exact quotation requires:

1. dossier `quote_status: quotation-ready`;
2. exact passage transcription with stable ID and locator;
3. linked record `citation_status: citation-ready`;
4. adequate edition/provenance, verification, and use boundary for the proposed use.

Other quote states are non-quoting states: `unverified`, `source-matched`, `locator-verified`, `paraphrase-only`, or `rejected`. Preserve the dossier's actual vocabulary when a foreign bundle differs.

Name the evidential relation when a source bears weight: `Extracted`, `Paraphrased`, `Argued-from`, or `Resonant-with`. These relations are not interchangeable.

## Export provenance

Every content node in the shipped bundle has:

- `canonical_path`: its originating path in the development workspace;
- `canonical_sha256`: the content fingerprint at export time.

These fields make the export auditable. They do not require the reader to possess the development workspace, and they do not override the exported node available at runtime.

## Body expectations

| Type | Expected body evidence |
|---|---|
| `section` | movement thesis, warrant-bearing development, limit or audit boundary, transition |
| `argument` | claim, warrants, tension/counterpressure, downstream opening |
| `concept` | definition, function in the argument, source boundary, related nodes |
| `source-record` | contribution, licensed use, readiness, claim boundary |
| `quote-dossier` | passage, stable ID, locator, verification, relation, use boundary |
| `path` / `braid` | ordered linked members and reason for the traversal |
| `index` | direct routes to every included node |

## The gate in one line

Orient at the essay package entry (`essay/README.md`; the field opens at `essay/symbolon/README.md`) → follow links to the claim's complete argumentative neighbourhood → preserve `claim_status` → independently check source-record `citation_status` and dossier `quote_status` before attribution or quotation → cite the file and line range actually used.
