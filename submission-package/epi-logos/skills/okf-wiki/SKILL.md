---
name: okf-wiki
description: "Use when researching, explaining, teaching, reviewing, or writing from a published Obsidian vault, linked Markdown work, or Markdown+YAML OKF bundle."
---

# OKF Wiki

Use the wiki as a connected work, not as a folder of excerpts. Discover the roles and relations present in the current release, then follow them until the proposition or image is understood in its neighbourhood. Do not assume a title, asset census, folder layout, or fixed set of node types.

The default bundle entry is `[plugin-root]/resources/essay-okf/index.md`. This skill lives at `[plugin-root]/skills/okf-wiki/SKILL.md`, so the same file is reachable as `../../resources/essay-okf/index.md`. If the user supplies another OKF bundle, use its `index.md` and schema instead. `$OKF_BUNDLE` may name that alternate root.

## The retrieval loop

Run this loop before substantive synthesis:

1. **Orient** — read the bundle entry or the reader's current vault page. Discover the available roles, links, embeds, headings, and paths.
2. **Find** — resolve the reader's named page, diagram, heading, or issue through the entry surface, local prose, captions, backlinks, and declared links. Do not infer relevance from filename or folder adjacency.
3. **Open** — read the whole entry page, including frontmatter where present, not only the matching paragraph.
4. **Expand** — follow ordinary Markdown links and embeds to the governing argument, incoming movement, outgoing movement, defined ideas, diagrams, and source material.
5. **Trace** — recover the proposition, warrant, tension or boundary, incoming dependency, outgoing consequence, and relevant source relation.
6. **Assemble** — retain a compact context packet containing the exact nodes and statuses needed for the answer. Compression may remove repetition; it must not erase disagreement, qualification, transition, or claim force.
7. **Verify** — apply the independent status gates below and re-open any file whose role or wording is uncertain.
8. **Act** — answer from the recovered trace, cite the bundle files used, and state any named context debt.

An index, search result, remembered phrase, or summary is a locator, never the proposition's authority. If the trace is incomplete, keep traversing. Do not repair a missing warrant or relation with fluent inference.

## Minimum context packet

Before explaining or developing an essay position, have these on the table:

- the home section or argument and its `claim_status`;
- the claim in its own wording;
- the warrant that earns it;
- its explicit tension, limit, counterpressure, or proof boundary;
- what the claim depends on and what it opens;
- every concept whose definition materially controls the claim;
- the relevant source record and quote dossier when scholarship is invoked;
- the coordinates or braid membership when they affect the reading.

This is the anti-loss rule. A short answer may be short because the trace is understood, never because the trace was skipped.

## Follow the graph by discovered role

Use the current index and page frontmatter to discover the roles the release actually contains. A manuscript or path carries declared sequence; a movement carries local development and transition; an argument carries a proposition and warrant; an idea fixes its local meaning; a diagram carries an image-operation; a source house carries bibliographic identity, learning material, passages, readiness, and use boundaries; supporting material remains subordinate to the pages that give it argumentative work.

The shipped snapshot presently consolidates source identity and passage material under `references/sources/`. Other vaults may use another layout. Resolve the linked source house from the page and its declared type rather than assuming a directory name.

Prefer a purposeful traversal over bulk reading: one live entry, the context that controls it, and the links that genuinely bear on the reader's question.

## Keep the five axes independent

1. **Node role and authority** — a source record, quote dossier, concept, and argument do different work.
2. **Claim force** — `claim_status`: `Derived`, `Argued`, `Offered`, or `Open`.
3. **Citation readiness** — `citation_status` on a source record. This licenses bibliographic attribution or paraphrase, not exact quotation.
4. **Quotation readiness** — `quote_status` on a quote dossier, together with the passage's locator, edition/provenance, verification, and use boundary.
5. **Retrieval confidence** — how completely the current traversal recovered the proposition's context.

Never use one axis to silently alter another. In particular:

- A retrieval gap does not demote an `Argued` or `Derived` essay position. Name the context debt and retrieve more.
- Missing citation or quotation readiness does not weaken an internally earned argument. It restricts what may be attributed or quoted.
- `Offered` must remain Offered; `Open` must remain open.
- Do not retreat from an earned position into generic academic hedging. State the essay's actual force, then state its actual boundary.
- Do not upgrade resonance into evidence or make a source author endorse the essay's inference.

When a source matters, preserve its declared relation: `Extracted`, `Paraphrased`, `Argued-from`, or `Resonant-with`.

## Quotation gate

Exact quotation is permitted only when all of the following are present in the available source house or linked passage object:

- `quote_status` is `quotation-ready`;
- the exact passage has a stable passage ID and locator;
- `citation_status` is `citation-ready`;
- edition, provenance, and the passage's use boundary support the proposed use.

Otherwise paraphrase, attribute only to the extent licensed by the record, and say that the exact wording is not quotation-ready when that distinction matters. Never reconstruct a quotation from memory, a section's paraphrase, or a source record.

## Provenance and citation

Every exported node carries `canonical_path` and `canonical_sha256`. These are trace receipts from the development workspace, not paths the reader runtime must be able to open. In the shipped runtime, the exported node is the available authority.

Cite the bundle file and exact line range, for example:

`resources/essay-okf/arguments/02-objective-internality.md:L18-L31`

Name the traversal when it helps the reader reproduce the reasoning: home argument → controlling concept → source record → quote dossier. Do not cite an index for a claim that lives in a section, or a record for wording that only appears in a dossier.

## Reader calibration

If the request is for a guided reading rather than research, route through `walk-the-essay`. It chooses the aperture and entry path; this skill still performs the traversal, status gate, and citation work.

For a large or index-less foreign bundle, run `references/okf-scan.py <root>` to inventory types, coordinates, statuses, links, and dangles. Read that bundle's own schema before interpreting custom fields. The scanner locates; it does not establish authority.

When the reader wants to retain or resume the route, read `../../resources/reader/TRAVERSAL-LEDGER.md` and hand the recovered events back to `walk-the-essay`. The ledger records the path taken; this skill continues to recover the work itself.

## Failure conditions

Stop and name the debt instead of improvising when:

- the claim's home node cannot be found;
- a referenced warrant, definition, transition, or source node is absent;
- the bundle contains conflicting status fields that cannot be resolved from its schema;
- exact quotation is requested without a quotation-ready dossier and citation-ready record;
- the proposed synthesis depends on a relation the graph does not state and the text does not argue.

Do not flatten coordinates: `#` is the Möbius parent, not position 4; P-family and L-family coordinates are not interchangeable. Do not confuse analogy with identity. Do not let stylistic caution hide what the essay has actually earned.

## References

- `references/okf-format.md` — portable node, status, provenance, and source-layer schema.
- `references/okf-scan.py` — fallback inventory for foreign bundles.
