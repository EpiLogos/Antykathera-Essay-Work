---
title: "The Return of Zero — Writing, Review, and Publication Protocol"
page_type: governing-writing-protocol
status: active-preliminary
authority: subordinate-to-central-plan
protocol_version: "1.0.0"
date: "2026-08-04"
publication: repository-governance
---

# The Return of Zero — Writing, Review, and Publication Protocol

## 1. Purpose and authority

This protocol governs the passage from the ratified development canon to the full written essay and its publishable Obsidian form. It separates preliminary preparation from prose production so that different writing models can work from the same ratified base under the same execution conditions.

The authority order remains:

1. `essay-workshop/the-return-of-zero-central-plan.md` — sole structural authority;
2. `essay-workshop/return-of-zero-orienting-principles.md` — mandatory orientation, subordinate to the plan;
3. live section, argument, concept, history, and traversal records — granular argument;
4. canonical source-house `SOURCE.md` files — evidence and source authority;
5. Frank-authored source-house `NOTES.md` files — readable, never agent-writable;
6. `essay-workshop/THE-RETURN-OF-ZERO.md` — sovereign manuscript;
7. this protocol — workflow and publication-shape authority, never argument authority;
8. generated rooms, indexes, ledgers, databases, and exports — locators or refractions only.

Where this protocol and the central plan diverge about the argument, the central plan wins. Where a generated surface and a canonical record diverge, the canonical record wins.

## 2. The non-duplication principle

The publication vault is the natural reorganisation of the work, not a generated likeness of it. A public record is therefore admitted by **ratifying and moving the record into its final place**, then updating its links, authority declarations, retrieval tools, and tests. It is not maintained as a second copy beside a supposedly more real internal original.

During the transition, `essay-workshop/` remains canonical. No file becomes public authority merely because a similarly named file exists under `symbolon/`. When migration begins, each record receives one declared canonical home and the former path is retired or retained only as explicit frozen provenance. Source quotations are never duplicated as convenience copies; their public use points to one admissible source record with preserved provenance.

## 3. Publication ontology and repository shape

The repository has one ontological publication body and several sibling support systems:

```text
/
├── README.md
├── WRITING-PROTOCOL.md
├── symbolon/
│   ├── README.md
│   ├── THE-RETURN-OF-ZERO.md          # after manuscript migration
│   ├── 0-1.md
│   ├── 1-0.md
│   ├── the-slash.md
│   ├── self-identity.md
│   ├── mono-poly.md
│   ├── complexio-oppositorum.md
│   ├── eight-determinations.md
│   ├── matheme/
│   │   ├── ql/
│   │   ├── spanda/
│   │   ├── topology/
│   │   ├── harmonics/
│   │   ├── formal-neighbours/
│   │   ├── computation/
│   │   └── diagrams/
│   ├── mytheme/
│   │   ├── myth/
│   │   ├── narrative/
│   │   ├── poetry/
│   │   ├── media/
│   │   ├── art/
│   │   ├── music/
│   │   └── plates/
│   └── episteme/
│       ├── sources/
│       ├── histories/
│       ├── etymologies/
│       ├── lenses/
│       ├── maps/
│       ├── dossiers/
│       └── figures/
├── essay-workshop/                    # development canon during transition
├── submission-package/                # manifest, companion, cards, release support
├── writing-guidance-tools/
├── tools/
└── tests/
```

The filenames shown for future Symbolon records express the required kind of direct placement; their final census and names are ratified from the canon, not frozen by this diagram.

There is **no `symbolon/relations/` directory**. `0/1`, `1/0`, the slash, self-identity, mono–poly, complexio oppositorum, the eight determinations, inversion, ground, mark, and return are the direct work of Symbolon and sit at its root. Introducing another container between Symbolon and these relations would turn the relation itself into a category beneath an index and would misstate the mathematics.

The three descending registers are:

- **Matheme** — the Spanda equations, QL derivations, formal notation, topology, harmonic and projective constructions, proof boundaries, and worked mathematical foundations.
- **Mytheme** — narrative, myth, poems, artistic operations, media references, cultural figures, and the forms through which a relation becomes liveable or perceptible.
- **Episteme** — source records, histories, etymologies, MEF lenses, essay and argument maps, comparative dossiers, evidence qualifications, and scholarly routes.

Symbolon does not become a fourth topical bucket beside these three. It is their holding relation and return. Its root records carry the operations by which the registers belong to one work without collapsing into one another.

The writing protocol remains at repository root. It governs Symbolon but is not Symbolon-content. Submission machinery, the reader companion, Epi-Card, validation reports, and release manifests also remain outside the `symbolon/` chain. Media remains beside its governing record: formal assets in `matheme/diagrams/`, composed imaginal assets in `mytheme/plates/`, and evidential visualisations in `episteme/figures/`.

## 4. Record identity, node type, and register

Folder placement does not replace record identity. Every admitted record declares independently:

- a stable `record_id`;
- its `record_type` — essay, movement, argument, concept, history, source, lens, map, path, poem, visual, or another ratified type;
- its `register` — symbolon, matheme, mytheme, episteme, or a declared cross-register composition;
- its `claim_status` where it makes a claim — Derived, Argued, Offered, or Open;
- its source relation where applicable — Extracted, Paraphrased, Argued from, or Resonant with;
- its canonical status and public status;
- exact essay and argument targets;
- outgoing and return relations.

The ontology carries the content by determining the record's home and relation. It does not erase the historical and argumentative node types that make that content intelligible.

One subject has one canonical public record unless two records perform genuinely different operations. Different filenames or folders are not sufficient grounds for duplication. A source record, a mathematical derivation, and a mythic treatment can address the same pressure because their register and work differ; three summary notes saying the same thing cannot.

## 5. Granular pointing and return

The essay must support linear reading without requiring a click. Depth records must support exact return without forcing the reader to hunt for the passage that called them.

Every stable manuscript location therefore receives a block identity at the smallest useful argumentative grain. The form is:

```text
^roz-s03-m27-claim04
```

The identity names the work, station, movement, and local claim. It remains stable across wording changes and changes only when the argument itself is divided, merged, or relocated.

Depth records declare one or more exact relations to those locations. The admitted relation vocabulary is:

- `derives`
- `grounds`
- `defines`
- `historicises`
- `sources`
- `qualifies`
- `tests`
- `figures`
- `embodies`
- `extends`
- `compares`
- `presages`
- `returns-to`

Each relation must identify an actual operation, not a shared keyword. Every depth record opens by naming the proposition or object it serves and closes with a readable route back to the precise essay or argument location. The essay carries the inverse link in prose: the sentence must explain why the reader may open the depth, not merely display a bare wikilink.

A substantial tangential record contains:

1. the positive proposition, object, history, or image it treats;
2. the operation it performs for the main argument;
3. its exact essay and argument targets;
4. what it adds that the essay properly compresses;
5. source and provenance boundaries;
6. claim, citation, quotation, and public-readiness status where applicable;
7. its Symbolon relation and register;
8. an explicit route of return.

A title, summary paragraph, backlink list, or graph position is not a depth record.

## 6. Phase P — preliminary work on `main`

All preliminary work occurs on `main`, in the ordinary working directory, with **no new writing worktrees**. Existing unrelated worktrees are not used by this protocol.

The quilt foundation is not part of the preliminary running order. Frank is reviewing and ratifying it separately. That ratification is recorded as a later content gate; it does not prevent the following work:

1. establish the root protocol and ontology-led vault shape;
2. keep the development authority and publication authority explicit during migration;
3. audit repository status, ignored files, source rights, and accidental private material;
4. make the architecture executable through real tests;
5. repair stale generated projections only when their canonical inputs are settled;
6. define the common model-run receipt and branch discipline;
7. define the public inclusion and exclusion contract;
8. restore GitHub authentication and create the public remote only after the history and rights gates pass.

Preliminary work does **not** include:

- drafting manuscript prose;
- producing final depth-record prose from unratified quilt material;
- classifying uncertain material merely to fill the new folders;
- producing final diagrams before their argumentative job is earned;
- creating model branches from different base commits;
- publishing the development history or private source corpus.

### Phase-P exit receipt

Before model branches are cut, `main` must record:

- the ratified quilt commit;
- passing real workspace and publication tests;
- the canonical packet version or content hashes;
- the writing-guidance version;
- the publication-schema version;
- the exact model list;
- the fixed execution parameters available in the runtime;
- the public-file and rights audit state;
- the intended repository name and authenticated GitHub owner.

## 7. Phase W — isolated model writing branches

Each complete model-written version receives its own branch:

```text
codex/write-<model-slug>
```

Every branch is cut from the **same ratified `main` commit**. Branches are used sequentially in the same working directory. The operator checks out one branch, completes and verifies that run, returns to `main`, and then checks out the next. No writing worktree is created. No model branch is rebased on, merged from, or shown the prose of another model branch before comparison.

The model identifier is the experimental variable. Every exposed execution parameter remains the same. Before the first branch is created, the common run receipt records these fields under the following rules:

| Field | Fixed rule |
|---|---|
| Protocol version | `1.0.0` |
| Base branch | `main` |
| Base commit | the single quilt-ratified commit used by every model branch |
| Branch | `codex/write-` followed by the actual model slug |
| Model identifier | the actual model identifier; this is the experimental variable |
| Reasoning effort | one exposed setting, identical across runs |
| Service tier | one exposed setting, identical across runs |
| Tool permissions | one permission profile, identical across runs |
| Network policy | one network policy, identical across runs |
| Context compaction | one recorded policy, identical across runs |
| Section order | canonical order |
| Fresh review roles | one fixed role sequence and timing |
| Tests | one fixed command list |
| Writing-guidance version | one commit or content hash |
| Canonical packet version | one commit and packet hash set |
| Publication-schema version | `1.0.0` |

Only values the runtime actually exposes may be claimed as controlled. Hidden temperature, sampling, routing, or subagent-model settings are not invented. If a fresh reviewer model cannot be selected explicitly, the receipt records the model actually reported by the runtime, when available, and names that variable as uncontrolled.

## 8. Canonical context packets

All writing models receive the same canonical material in the same order. A movement packet is a retrieval receipt, not a private summary. It identifies:

1. the movement and its canonical path;
2. inherited proposition and outgoing movement;
3. controlling arguments and concepts;
4. claim status and register;
5. warrant, source relations, and live proof boundary;
6. exact source houses and passage readiness;
7. relevant transverse threads and their full membership;
8. presages, withholdings, and later payoffs;
9. admitted authorial excerpts and visual tasks;
10. unresolved debt and the trace by which each item was reached.

When a source, concept, theorem, or transverse thread bears the passage, the effects map is run and the whole declared thread is read. Shared vocabulary never establishes a relation. For native QL notation, the core theorem spine and all eight determinations are recovered before a local token is interpreted. `X/x` remains Frank's authorial QL notation in every register.

## 9. Recursive reading and section production

Writing proceeds recursively from whole to part and back to whole:

```text
whole argument
  → station
    → movement
      → paragraph and exact source
    → movement plus both seams
  → station pair
→ whole manuscript changed by the passage
```

The governing model owns the branch and the sovereign manuscript. Fresh contexts or fresh agents perform bounded section and continuity work; they do not write concurrently into the same manuscript files.

For each movement:

1. read the whole essay's one-breath argument and current manuscript arc;
2. read the station as a complete movement;
3. read the target movement, its predecessor, and its successor;
4. recover every load-bearing argument, concept, source, history, and thread from canon;
5. state the local proposition, warrant, register, incoming pressure, and outgoing transformation;
6. draft the complete movement in a fresh writing context;
7. have a fresh seam reader inspect the preceding and following movement without defending the draft;
8. revise the seams and reread the whole station;
9. after each station pair, reread the manuscript from the beginning for accumulation, withheld disclosures, terminology, cadence, and return;
10. after the full draft, perform a cold whole-work read before any branch comparison.

Freshness is functional, not theatrical. A new agent or context receives the canonical packet and necessary adjacent prose, but not the drafting agent's self-justification or fault explanations. A section agent may propose prose or a patch; the branch owner admits it only after reading it in the whole. A seam reader judges what the reader actually receives. A whole-work reader judges the complete essay as one piece.

## 10. Writing laws and rubric load order

No single-pass prose ships. The writing-guidance load contract applies to manuscript prose, depth records, captions, plate text, public source commentary, and submission copy.

### Before drafting

Open:

1. `writing-guidance-tools/references/WRITING-LAWS.md`;
2. `writing-guidance-tools/references/WRITING-RUBRIC.md`;
3. the canonical packet, exact sources, outline, and existing essay text.

Keep closed:

- `fault-calibration.md`;
- `authentic-voice-reference.md`;
- `writing-style-reference.md`.

The draft begins from claim, warrant, dependency, register, and intended conclusion. Frank's examples do not generate the argument or pre-shape its surface voice.

The seven laws remain active throughout:

1. meaning before wording;
2. actors in subjects and actions in verbs, with passives retained when their reason is real;
3. give before use—operations and prerequisites before compressed identity;
4. make terms answer to stable referents and announce register shifts;
5. make difficulty earn itself and teach technical or foreign terms before they bear weight;
6. cut dead work while preserving living complexity, recursion, ambiguity, and length the thought requires;
7. let truth and achieved voice outrank mechanical compliance.

These laws carry Orwell's opposition to stale figures, needless length, removable words, avoidable passives, and unnecessary jargon, while retaining his final priority of judgment over rule. They carry ASD-STE's controlled meaning, explicit action, gradual presentation, and terminological stability without importing a sentence cap, vocabulary whitelist, passive ban, or technical-manual plainness into philosophical prose.

### During drafting

The rubric is used as a semantic checkpoint, not a sentence generator. At each completed movement, ask:

- G1: is the claim warranted at its stated strength?
- G2: are actor and operation legible?
- G3: have dependencies been given before compression?
- G4: does each paragraph perform one governing movement?
- G5: do terms retain their referents and registers?
- G6: has each difficulty been taught and earned?
- G7: does every negation answer a real position or boundary?
- G8: do opening and transition receive and transform what precedes them?
- G9: do compression and enumeration arrive only after work?
- G10: is the prose continuous with the essay's achieved voice, including explainable exceptions?

Checkpointing must not interrupt every sentence or reduce composition to fault avoidance. Complete the argumentative movement, then inspect it.

### Independent review

Calibration files remain closed. The reviewer first reads the whole relevant section in context, states its governing claim and each paragraph's work, and then audits G1–G10. Faults are recorded without rewriting in this form:

```text
location · fault code · exact phrase · failure · repair direction
```

The reviewer uses F1–F10 precisely: copula fraud, reflexive antithesis, nouned abstraction, sequence inversion, tour-guide narration, imported erudition, ungenerous opening, machine cadence, listing under compression, and prefabricated language.

The comparative and negation gate runs in the same independent pass. Every corrective negative or comparison answers four questions: who or what holds the first term; which exact operation separates the terms; why that difference matters here; and what information would be lost if the negative were deleted. Admissible forms are direct positive statement, source-bearing disagreement, operational distinction, and determinate or apophatic negation. Automated searches locate candidates only; they never establish faults or perform replacements.

### Selective calibration

Only after the independent fault ledger exists may the reviewer open:

- the matching section of `fault-calibration.md` for a specific fault code;
- the smallest relevant part of `authentic-voice-reference.md` for one named feature or edge in Frank's voice;
- one relevant passage in `writing-style-reference.md` for a defined craft problem.

The entire example corpus is never loaded by default. Calibration may confirm, reject, or refine a fault. It may not supply the essay's claim, create imported erudition, or license imitation of another author's surface manner.

### Revision and release

Repairs occur in this order:

1. false or unsupported meaning;
2. missing warrant and dependency;
3. unstable term or register;
4. paragraph movement;
5. sentence agency and operation;
6. cadence and diction.

Changed paragraphs are re-audited against all gates. Apparent violations may remain when their semantic or voice-bearing gain can be stated and a compliant version would lose it.

## 11. Frank's writings, poems, and first-person material

Frank-authored `[F]` blocks, the sovereign manuscript, poems, and Frank-authored `SCRATCH.md` or source-house `NOTES.md` remain sovereign. Agents do not rewrite poems, silently regularise them, complete fragments, or turn their diction into generic house style.

Each candidate use records:

- the authoritative internal source and exact locator;
- whether the use is a full poem, excerpt, title, allusion, image, structural echo, or voice calibration;
- the local argument or mythemic operation it performs;
- public permission and rights state;
- whether wording is exact, lightly normalised by Frank, or newly composed by Frank;
- its exact essay and register targets.

Poetry belongs chiefly to Mytheme when it figures, embodies, or lets a relation be experienced. It may cross into Symbolon when the poem itself holds the registers together, but that placement must be earned by its operation. A poem does not prove a formal or historical claim. Conversely, reducing a poem to an illustrative quotation destroys the work it may perform.

Frank's first-person accounts of AI encounter establish the authorial encounter and its phenomenological or methodological consequences. They do not, by themselves, establish machine phenomenality. External claims named within an authorial passage retain their own source and attribution burden.

Compression follows derivation. The main essay may use a short excerpt when the full work is available in a properly placed Mytheme record and the prose names why the excerpt enters. No excerpt is included merely to authenticate voice.

## 12. Matheme, Mytheme, Episteme, and Symbolon in prose

There is no quota requiring one carrier from each register in every section. Register admission is functional and polyphonic. A passage may need several mathematical carriers or none; several myths or none; a dense historical source braid or a direct derivation. Each admitted carrier must perform necessary, non-duplicative aletheia-work.

The register boundaries remain exact:

- Matheme derives, formalises, calculates, or marks a proof boundary.
- Mytheme figures, embodies, narrates, or makes a structure liveable.
- Episteme sources, historicises, compares, maps, qualifies, or teaches a body of knowledge.
- Symbolon holds the differentiated operations together and returns them without fusion.

A source cannot validate Frank's native theorem-language into existence. A myth cannot prove a matheme. A formal neighbour cannot be treated as historical identity. A cross-register relation is analogical or operational only after the distinct operation on each side has been recovered.

Complexity is managed by logical directness: state the positive proposition; show what acts and changes; teach the operation; admit only the carriers that alter understanding; then compress. The wealth of the archive belongs in exact depth records and return routes, not in a main paragraph swollen by names.

## 13. Diagrams, plates, figures, and media

A visual enters only when it performs argumentative or experiential work that prose alone would perform less exactly. Each admitted visual has a companion record declaring:

- stable `visual_id` and title;
- register and record type;
- exact essay blocks and argument nodes served;
- the operation or invariant made visible;
- source dependencies and claim status;
- diagram, plate, figure, map, facsimile, or artwork status;
- draft, verified, or final state;
- rights and licence state;
- caption and alt text;
- what the visual must not be taken to prove;
- forward and return links.

Formal derivation diagrams are governed from Matheme; mythic, narrative, poetic, and artistic plates from Mytheme; source, history, etymology, and argument maps from Episteme. A visual whose work is precisely to hold those operations together may be governed by a direct Symbolon record. The editable and rendered media files remain beside that governing record inside its register domain.

The essay earns each placement in prose before embedding the asset. The caption continues the argument without repeating the paragraph. Alt text communicates the visual's argumentative content, not merely its appearance. Rights-unclear assets do not ship.

## 14. Linear and holographic form

`THE-RETURN-OF-ZERO.md` remains one continuous, self-sufficient written piece. A reader who follows no link receives the entire argument, its necessary evidence, and its return.

The modular records make the same work readable radially, transversely, and toroidally:

- **linear** — the essay's declared sequence;
- **radial** — an exact essay block opening into its derivation, source, history, image, or implication;
- **transverse** — a declared relation or question followed across stations and registers;
- **toroidal** — a return to an earlier claim or image whose meaning has changed through the circuit.

Holography does not require every page to imitate one template. The whole relation may recur at the scale of essay, station, movement, record, diagram, and reader traversal while each scale keeps its own proportion.

Each public page carries a restrained local navigation field generated from declared relations only. The visible minigraph should normally show the present record, one incoming route, one onward route, and the few depth or transverse records necessary to orient the reader—usually no more than five to seven nodes. A text equivalent names the same routes. The global graph remains exploratory and never substitutes for prose-framed links.

## 15. Phase S — comparison, selection, and integration

Model branches are compared only after each has completed its full draft and verification sequence. Comparison begins from reader experience and argument fidelity, not model identity.

Each version receives:

1. a cold linear read of the whole essay;
2. a station and seam audit;
3. a source, quotation, attribution, and status audit;
4. a G1–G10 and comparative-negation audit;
5. a register and Symbolon audit;
6. a depth-link, return-route, minigraph, visual, accessibility, and rights audit;
7. a report of strengths, failures, unresolved debts, and deliberate exceptions.

Frank selects the primary version. Integration then occurs on:

```text
codex/written-edition-final
```

That branch begins from the selected complete version. Material from another model branch is imported only as a bounded, named improvement with its own seam, source, rubric, and whole-work reread. Model versions are not blended paragraph by paragraph merely to preserve contributions.

## 16. Public Git and clean-release discipline

The public remote is created only after:

- GitHub authentication is valid;
- the repository owner and public name are confirmed;
- source rights and Frank-private materials are audited;
- source-house `NOTES.md`, raw copyrighted copies, frozen development provenance, temporary rooms, rejected model drafts, run reports, caches, and machine-local files are excluded;
- the intended public tree passes link, asset, accessibility, and manifest tests;
- Git history is known not to expose files excluded from the current tree.

Deleting a private file in a later commit does not remove it from public history. If the present development history contains material that cannot be public, the release must begin from a clean public history of the reorganised final tree or undergo an explicitly approved history rewrite. Neither action is performed implicitly.

The public repository contains only what a reader or reviewer needs:

- root orientation and the writing protocol;
- the `symbolon/` vault;
- admitted assets and rights information;
- the submission manifest and genuinely submitted companion or card systems;
- minimal validation and publication tooling where it is part of the submitted work.

It excludes internal quilts, working ledgers, source-house `NOTES.md`, calibration corpora, legacy archives, raw rights-unclear source files, generated caches, model-comparison reports, and rejected drafts.

## 17. Verification gates

The work is ready for publication only when all of the following are true:

### Argument and prose

- the essay is complete and self-sufficient as one linear work;
- every movement preserves its inherited proposition, local operation, and outgoing transformation;
- withholdings arrive where earned;
- no evidence debt has softened or replaced the declared argument;
- the full rubric and comparative-negation gates pass after the final revision.

### Ontology and navigation

- Symbolon root relations live directly at `symbolon/`;
- Matheme, Mytheme, and Episteme contain records whose actual operation matches their placement;
- node type and register remain independent metadata;
- every depth record points to exact essay or argument locations and provides a route back;
- all wikilinks, embeds, backlinks, headings, and block references resolve;
- local minigraphs are derived from declared relations and have text equivalents.

### Sources, authorial material, and rights

- every quotation has a verified source, locator, and quotation status;
- every historical attribution stays within what the source establishes;
- every use of Frank's writing or poetry has exact provenance and permission;
- no Frank-authored `NOTES.md` has been agent-modified;
- every visual and media asset has its rights, caption, alt text, and non-claim boundary.

### Repository and release

- real tests exercise the actual vault, links, records, assets, and package commands;
- no mock, placeholder, or generated duplicate stands in for a canonical record;
- model branches share the same ratified base and exposed execution parameters;
- public files and Git history pass the privacy and rights audit;
- the public remote is authenticated, public, and connected only after these gates;
- the final published vault is the reorganised work itself, not a stale export of it.

## 18. Current preliminary state

As of 2026-08-04:

- the ontology-led `symbolon/` vault exists;
- Symbolon has no `relations/` layer and no separate `INDEX.md`;
- Matheme, Mytheme, and Episteme have complete functional domain trees and record contracts;
- this protocol is the live publication and writing workflow;
- the previous 2026-07-29 published-vault specification is retained only as design provenance;
- the working tree contains quilt-session changes and is not a safe base for model branches;
- GitHub identifies the intended account as `EpiLogos`, but its current CLI token is invalid;
- no public remote has been attached and no development history has been exposed.

The next content gate is Frank's quilt ratification. Once it is recorded on `main`, the repository can complete the move from `essay-workshop/` into the ontology-led homes, cut equal-base model branches, and begin the writing phase.
