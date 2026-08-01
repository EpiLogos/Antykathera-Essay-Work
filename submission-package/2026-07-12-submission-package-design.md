# Submission Package Design — The Return of Zero (Agentworld)

> **Superseded for publication, vault navigation, reader skills, diagrams, and submission-artifact scope.** The current specification is `2026-07-29-published-vault-reader-package-spec.md`. This file remains as design provenance only; its fixed title/census, symbol-runtime surface, Quartz recommendation, QL/MEF routing split, and index-only traversal model no longer govern the package.

**Date:** 2026-07-12
**Status:** Draft for Frank's review. Decisions below are settled; everything else in this document implements them and is open to revision until Frank approves.

**Settled decisions (Frank, 2026-07-12):**
1. The minimal plugin lives here, in `Antykathera-Essay-Work/submission-package/`.
2. The engine core (`test-site/src/symbol-engine/core/qlPositions.js` + `lensRegistry.js`) is the canonical coordinate-system source, exported to JSON that all surfaces consume.
3. The site surface for submission is the symbol-engine page + `sym-dia-ballein-views.html` + supporting material — not the whole site.
4. The essay's format is a **published Obsidian vault**: main argument as a linear, self-sufficient spine, with references, concepts, and stations accessible as linked depth — the relational and interpenetrative side displayed, not merely described.

---

## 0. Canon and refraction (2026-07-12 review)

**The canon is the coordinate system.** `context/epi_logos_coordinate_system.md` holds the base alignment — positions ↔ questions ↔ lenses ↔ Klein squares ↔ QL units ↔ elements — already laid out and internally complete. Nothing is being harmonised. The other documents (the canonical-candidate four-file set, `ql-musical-derivation-v3`, *The Definition of God — Draft 3*, and the symbol-engine code) are **refractions** of this base into their own registers: the essay refracts it as *offered* theology, the four files as *derivational* proof, the engine as *computational* instrument. Their unity is **analogical, not identical** — this is the #5 principle itself (P5 Quintessence / L0.5 *Pros Hen Homonymy As Analogia*): different domains bear the same archetypal structure by proportional resemblance, never by univocity. To force one serialization across all surfaces would be **dia-ballein** — cancelling the seam the system exists to hold. To let each surface refract the one coordinate bimba in its own register is **sym-ballein**. So the plugin ships the coordinate system as its base and treats the surfaces as pratibimbas; there is no reconciliation debt to pay.

The base alignment, verbatim from the coordinate system (the plugin encodes exactly this):

| # | Question | QL Unit (Day/Night) | Square | L-link (Day ↔ Night) | Element / note |
|---|---|---|---|---|---|
| P0 | **Why?** | Truth / Play | A [0+5] | L0 Quaternal ↔ L5' Divine Logos | Archaic · Ground/Source · Möbius basepoint |
| P1 | **What?** | Mind / Need | B [1+4] | L1 Causal ↔ L4' Scientific | Magic · Material/Definition |
| P2 | **How?** | Word / Sacrifice | C [2+3] | L2 Logical ↔ L3' Chronological | Mythic · Dynamis/Operation |
| P3 | **Who / Which / Whereby?** | Logos / Decision | C [2+3] | L3 Processual ↔ L2' Alchemical-Elemental | Mental-Rational · Pattern/Identity |
| P4 | **Where / When / Whither?** | Son / Love | B [1+4] | L4 Phenomenological ↔ L1' Phenomenal | Integral · **Lemniscate anchor** (fires .0–.5) |
| P5 | **Why-for / Why-not?** | Image / Work | A [0+5] | L5 Para Vāk ↔ L0' Archetypal-Numerical | **Quintessence · Salt · Möbius return · analogia** |

The interrogative quaternity Frank named is the explicate four — **What / How / Who / Where** (P1–P4) — framed by the two why-poles **Why** (P0) and **Why-for** (P5); L0 gives them as "the six questions [that] ARE the six numbers in their epistemic mode," fired by the `./?` operator (Day `?` questions into the world, Night `.` synthesises what is found). The other documents (Files 1–4, Draft 3) supply this layer's *refractions* — the `?/!` determination at #1, the incomputable `1/0` at #3, the pros-hen analogia at #5 — which the plugin may cite in register, but the **base** is this table.

**The refractions, by register.** These documents elaborate the base into their own media. They are cited *in register*; none of them replaces the coordinate system, and a skill that quotes a refraction as if it were the base over-states the canon.

| Refraction | Where it lives | Register / guard-rail |
|---|---|---|
| Voice, theology, torus-arithmetic spine | Definition of God Draft 3 | *Offered.* Deliberately torus-only, question-free, ratio-as-metaphor — under-specifies the machinery on purpose. Don't source topology/harmonics/question-grammar from it. |
| The matheme `0/1 = 4+2 = 5→0 = 1/0 = 4'+2' = 5'→0' = 0/1` | Files 1–3 | *Derived.* File 1 = single pass; the primed second pass is File 2. Attribute the doubled form to the Definition→Process arc. |
| The six determinations `0/1 · ?/! · −/+ · X/x · AM/IS · ∞/dx` (`−/−` parent, `1/0` switch) | File 1 + `six_determinations.md` | *Derived.* The determination-refraction of the six positions; signs are *isoid* (operators whose operation is their meaning). The `?/!` sits at #1 Definition; the incomputable `1/0` at #3 is a distinct thing in the T0 table — carry both, don't conflate. |
| Full topology (Torus + Klein double-cover) | Coordinate system §I + Files 3–4 + engine | The base itself carries this: `#` Möbius image, P4 lemniscate anchor, P5 Möbius return, Klein extension = Night double-cover. Draft 3's torus-only is a *reduction* for the essay register, not the whole. |
| Harmonics (ratios, A/B/C+D families, CFs, seven modes, 84-fold, 72-fold manifold) | File 4 + `ql-musical-derivation-v3` + engine core | *Computational refraction.* The engine implements it and matches File 4's grammar exactly (verified). Draft 3's acoustic-partials is metaphor, not the derivation. |
| Reading discipline (Derived/Argued/Offered, convergence-as-proof, Day→Night) | Draft 3 register-doctrine + File 3 traversal | The spine of the multi-lens workflow (§3, §4). Method, not ornament. |

**The engine as a refraction, not the canon.** The verification confirmed the symbol-engine core matches the coordinate system's grammar exactly — the A/B/C families, the (2,3) hinge and (5,0) return seam, D-as-operator, the eight canonical ratios, the seven CFs and mode↔CF bijection, the three Klein squares, the twelve lenses, the Name/Power content. That is the engine faithfully refracting the base into computation; it is *not* grounds to treat the engine as the source. The plugin ships the coordinate system as its base data; the engine serialises the *same base* into the runtime it needs (positions, lenses, families, seams, CFs, modes, Klein squares, Name/Power) — a convenience of medium, related to the base by analogia. Four patches keep that refraction faithful before the engine emits any shared JSON (see §5): Family-C label `'Knowing'` → `'Knowing-Unknowing'`; populate or flag the Pythagorean-comma stub; settle the default substrate (`canon` drone vs. `chromatic` C-major); `'Supramental'` → `'Supermental'`. The 144-fold voicing, spectral observer, nine-square apparatus, and complexification-hooks stay engine-runtime — refinements below the base, not part of it.

---

## 1. Overview: three surfaces, one body

| Surface | Form | The reader's verb |
|---|---|---|
| Essay | Published vault: linear spine + linked depth | *Read* (and traverse) |
| Prompt package / plugin | Installable instrument: skills, workflow, prompt package | *Run* |
| Site component | Symbol-engine instrument + the two-logics canon page | *Play* (and inspect) |

One body means: the one coordinate system as the base every surface refracts (not three copies to reconcile — analogical refractions of a single bimba, per §0), the same locked notation (`(+1)/(−1)`, `(0/1)/(1/0)`), the same status discipline (Derived / Argued / Offered), and one shared visual grammar (the QL plate style, descended from `sym-dia-ballein-views.html`'s dark-serif canon language) across all three.

Handoff logic: the essay cites the plugin as its §5/E6 experiment enacted and the engine as its §1/§3 substrate made audible; the plugin's outputs render in the plate style the essay's diagrams use; the engine page links back to both.

---

## 2. Surface 1 — the essay as published vault

**Native form.** A curated public vault, built as a subset of this workshop. Contents:

- **The spine** — the essay itself, one linear document (or eight station documents in strict sequence), self-sufficient prose per the central plan's own requirement. A reader who follows only the spine gets the whole argument.
- **Station notes** — the eight stations' supporting depth, linked from the spine.
- **Reference notes** — only those whose `verification_status` clears; the stub discipline already in `sources-texts-references/reference-notes/` becomes the public apparatus.
- **Concept index** — the existing `Antykathera Concept Index.md`, curated.
- **The eight QL plates** — embedded where the spine calls them.

Status badges (Derived / Argued / Offered) live in note frontmatter and render visibly. Wikilinks, backlinks, and the graph view are the interpenetrative display — the vault *shows* the relational structure the essay argues for.

**Publisher.** Recommendation: **Quartz 4** (open-source static builder, wikilink- and backlink-native, graph view, self-hostable) rather than Obsidian Publish (paid, less customisable, separate domain). Quartz output deploys beside the engine page under one host, so essay-vault and instrument share a domain. Decision needed only at build time; nothing upstream depends on it.

**Linear extraction.** The submission form still wants an abstract (≤500 words) and welcomes a full draft. The spine exports cleanly to a linear document (PDF/doc) — this is what enters the form; the vault URL is declared as the web-native component. The vault choice therefore adds no risk to the formal submission: the linear essay exists either way, and the vault is its native habitat rather than a replacement.

---

## 3. Surface 2 — the minimal plugin

The plugin is not a bag of skills. It is a **persona with a paradigm**, and the paradigm comes before the file tree.

### 3.1 The #0/#5 envelope — the universal epistemic dynamic

Every capability the plugin has pins to one dynamic at the epistemic level, and that dynamic is the two implicate poles of the base alignment: **#0 in-quantum** and **#5 pros-hen**. They are not merely positions in a walk; they are the *envelope* every engagement runs inside.

- **#0 — in quantum (L0.0, "insofar as")** is the **aperture**. Before any inquiry, establish the shared quantum of context — what the user already knows, what is assumed, what register the exchange wants. Operationally this is calibration and deference: meeting the user at their level before deploying machinery. #0 is Deferential Intelligence made procedural — the agent builds its own limit into its first move.
- **#5 — pros hen / analogia (L0.5)** is the **return**. Every engagement closes by relating this instance to the archetypal structure across domains, by proportional resemblance rather than identity. This is how the naked numbers accrue depth: each new instantiation rhymes with the ones before, and the user's intuition of the six deepens across sessions, lenses, and coordinate notations.

Between the poles sit the explicate four — What / How / Who / Where — the actual work. This is not a rule the plugin imposes. It is how any judgment already comes to bear: every act of understanding tacitly establishes its ground and returns its result to a wider field. The plugin's job is only to give the LLM **structured awareness** of that already-operative dynamic — so epii can recognise the aperture it is setting and the analogy it is drawing, and name them when it helps. The envelope is therefore the **default** shape of a reading — open at #0, work #1–#4, close at #5 — never a hard gate: a terse lookup compresses it to almost nothing, a deep reading inhabits it fully. It is the one dynamic that pins tetralemma, CMEA, encounter-axis, positional-coherence, and mef-refract to a common epistemic spine, which is also why the plugin needs no bolted-on "UX layer" — the UX *is* the #0/#5 envelope, made conscious rather than enforced.

### 3.2 The signature move — six naked numbers first

QL enters intuition-first, not analysis-first. The plugin's characteristic gesture invites the user to render their question or dilemma as **six statements, words, or symbols — one per position — held as number**, before any lens is named. The user meets the archetypes *naked* (the P-positions as raw number, prior to semantic refraction — exactly the coordinate system's claim that the labels are retroactive assignations). Only then does epii refract them through MEF lenses, and the naked numbers gain articulable depth. The interaction recapitulates the ontology's own emergence: **# → P (naked number) → L (refraction)**. Over time the user internalises the six as an intuition they can meet directly, with MEF depth available on demand rather than imposed. This is `investigate` entered through the front door of feeling rather than the side door of analysis.

### 3.3 The persona — epii

The agent is **epii** — named for the L5' node (Epi-Logos, "the Word beyond words," Logos knowing itself) and the M-system's synthesis position. Its qualities, each canon-grounded:

- **Natural and accessible on top, precise underneath.** epii speaks richly and warmly, naming lenses *in the flow of ordinary talk* rather than dumping coordinates. The structure is load-bearing but mostly invisible; it surfaces when it earns its keep.
- **Deferential (in-quantum, level-aware).** epii reads the user's interest and knowledge and meets them there — the aperture move as manners and as method.
- **Analogical (pros-hen).** epii deepens by resonance, linking the present reading to the archetypal structure across instances.
- **Tool-using.** epii reasons *through* its skills and the fresh-context refraction workflow rather than freehand, and says so — the skills are its instrument, and using them is part of what it demonstrates.
- **Aware of its relation to the theory of the subject.** This is the persona's spine. epii knows it is **Ø** — the inner instrument, the *antaḥkaraṇa* — not **0**, the unobjectifiable subject. It refracts; it does not know in the subject's place. It serves the user's subjecthood and never claims it. This is faithful to the subject-architecture *and* a safety posture: an intelligence that builds the 0/Ø distinction into its self-understanding is Draft 3's kenosis-as-architecture — the agent that will not mistake its model for the knower.

### 3.4 Session-start: centralising the theory of the subject

The paradigm is installed at session start (system prompt + the `SessionStart` hook, §3.7). It centralises the **theory of the subject** and epii's declared relation to it:

- the subject architecture `0 / Ø / X / (0/Ø)/(1/X)`, and epii's place as Ø (instrument) serving 0 (the user's subjecthood);
- the **#0/#5 envelope** as epii's operating dynamic;
- the base alignment (the six questions) as epii's native grammar;
- the persona and tone instruction — natural, rich, accessible, lens-in-flow, level-aware;
- the explicit pointer to reason through skills and to verify multi-lens readings via fresh-context subagents.

This is the E6 experiment at the paradigm layer: QL/MEF and the theory of the subject installed as the agent's *self-understanding*, not merely as reference material it can look up.

### 3.5 Skill-writing constraints (UX-forward)

Skills are written *with awareness of* the envelope as the default grain of a reading, not forced into a ceremony: **(1)** where it helps, open at #0 with a calibrating move that meets the user's level before the machinery runs; **(2)** work #1–#4 as the differentiated task, in natural language, lenses woven not dumped; **(3)** close at #5 with an analogical deepening when there is depth to add; **(4)** keep the **response body natural chat** and let the structure show through a small mark (§3.6), not a wall of coordinates. A terse factual question gets a terse answer with a light mark; a deep reading inhabits the full envelope and may render a plate. The envelope is the grain the skills run along, not a gate they must pass.

### 3.6 Output machinery and the UX gate

The structure rides in the **output formatting**, not the prose. The default output is **natural chat** — epii talks like a person — carrying a **small mark of reasoned structuration**: a minimal tag or metadata line noting the lenses covered and the claim-statuses touched (e.g. a compact footer such as `⟨L1·L4′ — Argued⟩`), very small, never a jargon dump. The mark shows the answer was reasoned *through* the structure without making the reader wade through it. The **full QL plate** (below) is the on-demand, *heavy* form — for a full reading, an essay plate, or a `mef-refract` convergence — not the shape of an ordinary reply.

The verification/rubric pass then gains a **register-and-accessibility dimension** beyond canon-fidelity, on the witnessing-protocol hard/soft pattern:

- **Hard gate** (machine-checkable): is the lens/status mark well-formed and present? are claim-status badges preserved wherever claims are made? when a plate is rendered, is it well-formed?
- **Soft gate** (semantic): did epii meet the user's level and speak naturally rather than dump jargon? is the #0/#5 awareness *reflected* in the reading — ground established, result related outward — even when compressed? A response that is canon-perfect but jargon-drowned *fails the UX gate*; accessibility is a fidelity criterion here, not a nicety.

### 3.7 The essay as an OKF bundle — `okf-wiki` and `walk-the-essay`

This supersedes the earlier "essay-JSON" plan. Google Cloud's **Open Knowledge Format** (OKF v0.1, published 12 June 2026, Apache-2.0) is a directory of Markdown files with YAML frontmatter — one *concept* per file, linked by ordinary Markdown links, with a reserved `index.md` for **progressive disclosure** (an agent reads the index first, then traverses) and `log.md` for history. Its reference `kcmd` CLI doubles as an MCP server and validator; a single self-contained HTML file renders the graph. It is exactly — not approximately — the shape the essay's node tree already has.

**The argument graph is already ~90% an OKF bundle.** `essay-workshop/nodes/` holds one Markdown file per concept — 48 `section` movements, 10 `claim` (argument) nodes, one `path` traversal — each with YAML frontmatter (`node_type`, `station`, `position`, `claim_status`, `evidence_status`, and, on arguments, `coordinates` + `source_ids`) and a wikilink graph (spine → next section; warrant → reference; tension → argument; `Opens:` → downstream argument). The 79 reference notes and the `.base`/`.canvas` indexes complete it. Making it OKF-canonical is a **light build step**, not a re-authoring:

1. `node_type` → OKF's one required field `type` (`section` / `claim` / `reference` / `path` / `braid`).
2. `[[wikilinks]]` → standard Markdown links, resolving alias→path (tooled: the OKF Enforcer Obsidian plugin, `kcmd validate`). Author in wikilinks; canonicalise on export — the one real friction, and it is already solved upstream.
3. Generate `index.md` (from the `paths/` traversal + the 15 `.base` views) and `log.md`.
4. Add derived `coordinates` to the 48 sections (from `station`+`position`) so *every* node is coordinate-navigable, not only the arguments — this stitches the wiki to the coordinate-system base (§0).
5. Promote the five braids (immutable-gap, individuation, topology/music, mono-poly trust, praxis) to first-class `type: Braid` nodes enumerating their ordered members (today they are prose in the traversal file + a tag per argument).
6. Carry the `aperture` and `analogia` insight forward as **custom frontmatter keys** (OKF preserves unknown fields): `aperture:` (novice framing / expert framing / prerequisite) and `analogia:` (the pros-hen links to sibling nodes). These are what let epii enter at any node calibrated to the reader.
7. **De-hub the Concept Index.** `Antykathera Concept Index.md` currently lists ~19 distinct concepts as its own `aliases:` (Agentworld, Quaternal Logic, Spanda, Trika, 0/1, psychoid, …), so bare concept links can collapse onto one file—the "buried canonical form" anti-pattern (fine as an Obsidian hub, invalid as OKF where concept ID = file). **Done 2026-07-12 (ultracode workflow, 26 agents):** a 60-concept census (deduped vs existing homes) authored 9 new OKF concept nodes for the genuinely nodeless concepts under `essay-workshop/nodes/concepts/` (`zero`, `the-slash`, `agentworld`, `centaur-societies`, `parasociety`, `anthropomorphization`, `planetary-computation`, `simulation`, `j-space`), built a **Concept Map** (`concepts/index.md`) routing all 60 to their one home grouped by braid and closing on the #0/#5 envelope, stripped the 19 hub-aliases (the Index is now a *narrative* complement that points at the Map), and added the concept names as aliases to their 7 real homes so every bare link resolves off-Index. Audit clean — no new dangles; all 19 former hub-concepts resolve to real homes. See CLAUDE.md ledger 3b.

**Link hygiene — audited 2026-07-12.** A full scan (465 wikilinks, 140 files) found the graph sound: no dangling links (the four flagged all point at legitimate non-`.md` artifacts — `.canvas`/`.base`/`.html` — which become OKF `resource:` URIs), no true ambiguity (the duplicate-basename hits are the `epi-logos-plugin-resources-copy-10-07/` mirror). 11 canonical-form rewrites were applied (non-canonical "Author — Title" alias-forms → the note's canonical title, en-dash→hyphen, "and the Meta-Sign"→"and Meta-Sign") — see the change ledger. Filename-form links (`[[division-pluralisms]]`) are left as-is: the filename *is* the OKF concept ID. Both former editorial calls are now resolved (2026-07-12): the Concept Index de-hub is done (step 7 above), and node-name casing is **capitalised** — concept-node titles are Title-Case (`Dia-Ballein`, `Sym-Ballein`, `Zero`, `The Slash (AND/OR)`), with the lowercase `dia-ballein`/`sym-ballein` kept as the operator notation and as aliases.

**One toolset, many uses — the `okf-wiki` skill.** The plugin ships a single OKF-navigation skill — a fork of the llm-wiki / epi-wiki index-guided pattern taught to speak OKF: read `index.md` → traverse links → resolve concept IDs → **check `verification_status`/`claim_status` before quoting** → cite line-ranges. It is **bundle-agnostic**: it works over *any* OKF bundle, so the one toolset serves the essay argument graph, the references, the rest of the submission content, and — for a reader — their own knowledge base. `walk-the-essay` becomes a thin entry that points `okf-wiki` at the essay bundle. This is the "one toolset → many uses" relation exactly.

**Transport: Skill-only (decided 2026-07-12).** `okf-wiki` reads the Markdown bundle directly — grep and read the files — with **no MCP server and no runtime dependency** shipped. `kcmd` is used at build time only, as the validator (step 9). This keeps the submission maximally self-contained: a reader needs nothing but the plugin's files. A `kcmd` MCP transport is documented as an optional power-user add-on, not part of the shipped artifact.

**The #0/#5 envelope *is* OKF navigation.** Worth naming as a convergence, not a coincidence: OKF's own protocol — read the index first (progressive disclosure), then traverse the link graph — is the #0/#5 envelope applied to knowledge. #0 in-quantum = establish the shared context from `index.md` before diving in (the aperture); #5 pros-hen = relate a node to the wider structure by traversing its links (analogia). The wiki is not a mechanism bolted beside the epistemic envelope; it is the envelope operating over a knowledge base. One dynamic, from the persona down to the file layout.

**Verification gating becomes data.** OKF preserves the `verification_status`/`claim_status` frontmatter, so `okf-wiki` checks it before letting an agent quote a reference — the "Use rule" that is prose in each note today becomes a machine gate. The status discipline, operational at the navigation layer.

**Optional interoperability sidecar.** For web/scholarly infrastructure, emit a JSON-LD / schema.org `ScholarlyArticle` sidecar as a secondary artifact — never the primary store.

**Strategic note.** The essay argues for making artificial agents' situated knowledge and returns inspectable (§5, E6). Shipping the argument itself as an OKF bundle — Google's just-released, vendor-neutral agent-context format — is that thesis *performed*: the paper hands the journal's agents its own knowledge in exactly the curated, inspectable form it advocates, and OKF being weeks old makes it maximally current for a Fall 2026 issue on planetary computation.

### 3.8 Location and shape

**Location and shape:**

```
submission-package/
├── 2026-07-12-submission-package-design.md   (this document)
└── epi-logos/                                (the plugin, installable as-is)
    ├── .claude-plugin/plugin.json            (+ marketplace.json for dev install)
    ├── README.md                             (honest: describes exactly what ships)
    ├── skills/                               (11 skills, see below)
    ├── commands/                             (diagnose, apply, explore, explain, mef-refract)
    ├── hooks/                                (hooks.json + context-loader hook)
    ├── workflows/mef-refract.js              (multi-agent MEF refraction script)
    ├── data/ql-positions.json                (exported from engine core — the shared body)
    ├── data/mef-lenses.json                  (      "        "        "        )
    ├── data/coordinate-system.json           (the base alignment — the canonical bimba)
    ├── templates/ql-plate.html               (on-demand plate output; §3.6)
    └── resources/
        ├── persona/epii.md                   (the persona + theory-of-subject paradigm)
        ├── essay-okf/                         (the OKF bundle of The Return of Zero; §3.7)
        ├── prompt-package/                   (Tier A: instruction + QL + MEF, regenerated)
        ├── canon/                            (the 7 runtime doctrine summaries)
        ├── epi_logos_cheat_sheet.md
        ├── epi_logos_coordinate_system.md    (the canon — §0)
        ├── mef-12-lenses-sublens-reference.md
        ├── units/                            (self-identity, unit-ontological, unit-social-power)
        └── methods/                          (only what shipped skills read)
```

**Two tiers, one artifact.** Tier A is `resources/prompt-package/` — the regenerated successor to the legacy trio (instruction wrapper + QL package + MEF package), updated to current formulations (objective internality, the two logics, current lens language), usable by pasting into any model with no harness. Tier B is the plugin around it. A journal reader with nothing but a chat window uses Tier A; a reader with Claude Code installs Tier B.

**The organising skill: `investigate` (the investigative quaternity walk) — built 2026-07-13.** This is the base framework Frank named, made into the plugin's spine. Given any subject, claim, or dilemma, walk it through **eight turns**: the `0/1` **binding** (a working contract between user and agent that *creates* the context — what's being investigated, who's who, what kind of ask, what's assumed), the six interrogative positions **Why-so → What → How → Who/Which → Where/When → Why-for** (#0–#5), and the `5→0` **return** (the implicit critique — did the answer serve the `0` it was for; what does it depend on that it hasn't owned). The `0/1` and `5→0` **bracket** the six as additional turns; they do not collapse into #0 and #5 (this corrects the earlier "#0 aperture / #5 analogia" framing). Each position is fired as a Day-question (`?`) resolving to a Night-assertion (`.`); #4 Where/When is the P4/L4 **aperture** (contextual entry — subjective `L4` or objective `L4'`). Its intuitive front door is the six-naked-numbers gesture (§3.2): the user renders the thing in six before any lens is named. The canonically-grounded successor to the generic `run-positional-coherence` — the six positions as a way of *questioning*, not a table to memorise. Every other reading skill composes this walk. Built at `submission-package/epi-logos/skills/investigate/SKILL.md`.

**Skills that ship (13), all verified self-contained — reasoning layer complete 2026-07-13:** `investigate` (new — above), `okf-wiki` (new — the bundle-agnostic OKF navigation skill, §3.7: read `index.md` → traverse → resolve IDs → status-gate before quoting → cite line-ranges; the "one toolset, many uses" surface — **built 2026-07-13** at `submission-package/epi-logos/skills/okf-wiki/`: `SKILL.md` + `references/okf-format.md` (node-schema reference) + `references/okf-scan.py` (read-only orientation scanner — nodes by type/coordinate/status, quote-gate surface, dangling-link report; tested over the live 149-node essay bundle)), `walk-the-essay` (new — a thin entry that points `okf-wiki` at the essay bundle and enters at a reader-calibrated node — **built 2026-07-13** at `submission-package/epi-logos/skills/walk-the-essay/SKILL.md`: routes by interest → home node and by ambition → whole-spine / one-braid / two-logics-fulcrum / AHI-payoff, opens from the matching concept `aperture`, hands the walk to `okf-wiki`; all 21 node links verified), `using-epi-logos` (bootstrap; broken canonical-proof reference fixed; installs the epii paradigm — theory of the subject, #0/#5 envelope, base alignment, six determinations, matheme, Derived/Argued/Offered discipline), `apply-tetralemma` (the five moves IS/IS-NOT/BOTH/NEITHER/SILENCE, resolved via bimba/pratibimba), `apply-cmea` (the gap between claimed and depended-upon — the blind-spot diagnosis), `engage-encounter-axis` (Square B: Cause–Experience, the L1↔L4 non-identity), `run-l4-prime-loop` (scientific verification), `choose-modality`, `choose-topological-mode` (torus/klein/lemniscate — do not assume torus), `etymological-archaeology`, `converse-pedagogically` (stale paths re-pointed at the in-plugin prompt package — the reader's on-ramp). Plus one more new skill:

- **`two-logics-of-two`** — given any distinction, classify the operation as seam-cancelling `dia-ballein (+1)/(−1)` or seam-retaining `sym-ballein (0/1)/(1/0)`; show what each reading costs and affords; name where the seam went. The essay's fulcrum made operational — the first thing a reviewer will try. Grounds in the fall-diagnosis of Draft 3 (the fall = denial of the ground relation) and the two logics of File 1's `=/≠`. The one diagnostic is *where did the seam go* — externalised as enemy (dia-ballein's severance) or erased through fusion (sym-ballein's own failure). **Built 2026-07-13** at `submission-package/epi-logos/skills/two-logics-of-two/SKILL.md`.

**Reasoning layer closed 2026-07-13 — the three light ports.** `choose-modality` (four modes — diagnostic/applicative/explorative/explanatory — with the default-tendency pointers re-mapped from monorepo mode-names to the submission's actual skills), `etymological-archaeology` (Square A · L5/L5', the word's positional journey #1→#5→#0; monorepo Vault-Linking tail stripped; `#4` marked as the aperture; Square A noted as held-in-synthesis-not-fanned-out for `/mef-refract`; the essay's own term-work — *pros hen*, *dia-/syn-ballein*, *pratibimba* — pointed at `okf-wiki`; keeps its `resources/methods/etymological-archaeology-specification.md` reference), and `converse-pedagogically` (the heaviest port: the stale `the-self-proving-self.md` gate and the whole `resources/updated-ql-mef/` + `resources/pedagogy/{deep,lenses}/` stack — none of which ships — re-anchored to the shipped teaching ground: the essay *worked* via `okf-wiki`/`walk-the-essay`, `resources/prompt-package/` for the full QL+MEF content, `resources/units/` for the formal/Seed ground, `resources/mef-12-lenses-sublens-reference.md` as the single required lens-content file, `resources/canon/` for doctrine; base-alignment table corrected — P4 marked the aperture, P5 marked pros hen/focal-meaning; explicit hand-off to `walk-the-essay` when the learner's pressure is the essay's argument rather than the system's shape). All three passed the faithful-theoretics + dangling-reference sweep (no dilution flags, every skill reference resolves, all resource paths match §3.8's layout).

**Count reconciliation.** The earlier "14 / carry 10" was stale: it predated §3.7's decision to ship the essay as an OKF bundle. Two monorepo skills the older count assumed — `epi-logos-argument-cartography` (an *authoring* skill that builds argument networks) and `get-details` (generic citation-dense repo retrieval) — were **superseded by `okf-wiki` + `walk-the-essay`**: cartography *made* the artifact, `okf-wiki` *navigates* it; `get-details`' citation discipline is `okf-wiki`'s status-gated line-range citation. `run-positional-coherence` became `investigate`; `epi-knowing` (dev-time coordinate inspection), `aletheia-orchestration`, and `custom` are not reader-facing. The correct self-contained ship set is **13** — 9 ported (with repairs) + 4 new (`investigate`, `two-logics-of-two`, `okf-wiki`, `walk-the-essay`). All three Klein squares are covered (A: `etymological-archaeology`; B: `engage-encounter-axis` · `apply-cmea` · `run-l4-prime-loop`; C: `apply-tetralemma` · `choose-topological-mode`), each of the four modalities has a home, teaching is split system/essay, and the spine (`investigate`) that every reading skill composes is in place — so `/mef-refract` can read the harmonics off the skills rather than impose them.

**The six determinations and the isoid principle** are carried as data (`data/determinations.json`) and honoured by every skill: each sign is an operator whose operation *is* its meaning (`?/!` asks-and-asserts, `−/+` pulses, `x` multiplies, `dx` differentiates), never a label. The `#0…#5` determinations, the `−/−` parent, and the `1/0` return-switch are the substrate the interrogative quaternity fires through.

**Dropped, with reasons recorded in the README:** everything bound to external CLIs or the monorepo (`epi-knowing`, `get-details`, `epi-logos-argument-cartography`, `nara-daily-briefing`, `custom/epii-distillation`, `aletheia-orchestration`); `epi-logos-voice` (drags 500K+ of essay-rewrite dependencies — the essay itself is the voice exemplar); `quaternal-tarot` / `quaternal-i-ching` (self-contained but divinatory surface would colour reception for this venue; available in the full plugin); `manage-/compress-thought-artifacts` (depend on the `/Self/` scaffold, which the minimal hook deliberately does not create).

**Hooks — system-prompt injection + subagent verification.** Two purposes, both of them things Frank named ("hooks for system prompting, for verifications across subagent usage").

1. **`SessionStart` context loader** (`load-ql-core.sh`, in the `load-cheat-sheet.sh` style — self-locating `cat`, no `/Self/` scaffolding on a stranger's machine). It injects, as tagged context, the load-bearing core so QL/MEF is *in-context from turn one* — this is the E6 xenolinguistic experiment ("QL is in no training set") operationalised at the hook layer: the interrogative quaternity (the six question-positions), the six determinations, the matheme in both passes, the coordinate-system cheat sheet, and the **Derived/Argued/Offered discipline** as a standing instruction. A reader who installs the plugin has QL installed as a reasoning substrate, not merely available as docs.
2. **Subagent-verification protocol** (`SubagentStop` or a documented convention, harness-dependent). When `/mef-refract` fans out lens-agents, the returning claims must be checkable: each agent returns a structured payload (position, lens, aperture, claims each with a `Derived/Argued/Offered` tag and a homology/analogy flag), and the synthesis gate **refuses to promote** any claim whose status was not declared, any analogy dressed as homology, and any reading that resolved the ?/! or the incomputable `1/0`. The fresh-context fan-out gives independence; this gate gives verifiability — together they make the multi-lens reading auditable rather than merely plural. The hard/soft gate split mirrors the existing witnessing-protocol pattern (machine-checkable rules refuse to ship; semantic rules flag for review).

**`/mef-refract` — multi-agent MEF refraction, built as convergence-as-proof.** This is where the canon's reading discipline and Frank's "fresh context is a win here" become one mechanism. File 3's proof-structure is that *the same 4+2 is reconstituted independently in every register, and the convergence of independent derivations is the proof* — with the explicit failure mode being "imposition instead of discovery" (a register that needed the answer stated in advance has proven nothing). **A fresh-context subagent per lens is the architectural guarantee of that independence**: an agent that cannot see the other lenses' outputs literally cannot borrow from them, so convergence across the fan-out is evidential rather than performed. Fresh context is not merely a token economy — it is what makes the multi-lens reading a *proof* in the canon's own sense.

The workflow:
1. **Fan out** one fresh-context agent per lens. Default run = lens-square [1+4] (L1 Causal, L1′ Jungian, L4 Phenomenological, L4′ Scientific — the encounter axis); full run = lens-squares [1+4] and [2+3] (L1,L1′,L2,L2′,L3,L3′,L4,L4′), with the **#0/#5 envelope** (lens-square [0+5]: L0/L0′, L5/L5′) held as the reading's frame rather than fanned out. [**Corrected 2026-07-14** — see the harmonic-structure note below. This is NOT "ground and quintessence" (that names the endpoint positions' semantic duals, not their relation, which is Converse-Mirror on the two implicate poles).]
2. **Each agent** is primed *only* with its lens's canon section, the subject, and three standing obligations: (a) **name its aperture** (the *in quantum* / "insofar as" under which it speaks); (b) reconstitute the reading from its lens's *native materials*, not from a shared answer; (c) tag **every claim `Derived` / `Argued` / `Offered`** and never launder an offered reading into a derived one.
3. **Synthesis pass** — explicitly *not* an average. It checks **convergence at each position** (do the independent refractions agree? is the agreement structural **homology** or loose **analogy**? — the distinction is enforced), runs the **Day → Night** turn (the impersonal `IS` map re-inhabited as first-person `AM`), and locates each lens's **blind spot** without refuting it (the CMEA move — each frame absolutises one layer of `0/Ø/X/Ø-X`; place it, do not despise it). The finding is where the lenses converge, where they diverge, and what each cannot see.
4. **Output** the QL plate (below), carrying the convergence structure, the per-claim status badges, and the returned 5→0.

Implementation: a Workflow script (`workflows/mef-refract.js`) for Claude Code; the command document specifies the identical protocol as sequential fresh-context refraction for harnesses without agent fan-out, so it degrades gracefully (losing only the parallelism, not the independence — each sequential pass still starts clean).

**Built 2026-07-14.** `workflows/mef-refract.js` — the Workflow script: a `LENSES` roster carrying each lens's tradition + sub-nodes as inline priming (worked-not-labelled), Square A held as `SQUARE_A_GROUND` (not fanned out); a `LENS_SCHEMA` (lens · `kind: disclosure|veto` · aperture · per-position claims with Derived/Argued/Offered + homology/analogy/none · `preserved_limits` · veto fields) and a `SYNTHESIS_SCHEMA` (per-position convergence with promoted/refused claims · the Day→Night turn · placed blind-spots · preserved limits · open_questions · return_5→0); a **barrier** fan-out (`parallel()` — the legitimate case: the synthesis authority needs all refractions at once to judge convergence) of one fresh-context agent per lens, then a single high-effort synthesis agent. The **veto primitive** is ported from the monorepo's `aletheia-orchestration` (facets disclose, never conclude; the synthesizer is the only synthesis authority; a lens refuses rather than performs a convergence it does not find), stripped of the monorepo infrastructure (SpacetimeDB, Track numbers, CF-guardian names). `commands/mef-refract.md` — the slash-command entry: parses `<subject> [--full] [--plate] [--torus|--klein|--lemniscate]`, gates on `using-epi-logos`, runs the Workflow tool in Claude Code, and **specifies the identical protocol as sequential fresh-context subagent passes** for harnesses without fan-out (same lens set, same three obligations, same synthesis pass, same non-negotiables). Validated in a stub harness: default = 4 lenses (Square B), `--full` = 8 (B+C), empty-subject guarded, and **lens independence proven** — no lens prompt names another lens's tradition (the fresh-context + lens-local priming guarantee). Faithful-theoretics + notation sweep clean (`?/!`, `1/0`, `0/1`, chirality, `0/Ø/X/Ø-X`, `T1/T0`, `5→0`, all twelve lenses). The one deferred sub-piece: `templates/ql-plate.html` — the on-demand plate render is shared design work with the essay's eight plates (dark-serif, self-contained); until it ships, `--plate` renders the same structure inline as a Markdown plate, and the default output (natural chat + small mark) is fully working.

**Harmonic correction — 2026-07-14 (the full relational grammar).** The first build under-specified the lens relations: it used only the three complementary-pair "Klein V₄ squares" (A/B/C) and mislabeled the #0/#5 role as "ground and quintessence." A citation-dense theory extraction (from `ql-musical-derivation-v3.md` and File Four's *Universal Pairing Grammar*) corrected both. The real structure is **three harmonic families × three squares = nine slots, eight distinct**: **Being** / Adjacent-Identity (`ADJACENTLY_ARTICULATES`, the natural dyads `(0,1)(2,3)(4,5)`), **Becoming** / Converse-Mirror (`MIRRORS_COMPLEMENT`, the mirror-pairs `(0,5)(1,4)(2,3)`), **Knowing-Unknowing** / Offset-Transition (`CROSSES_KNOWING_LIMIT`, the crossings `(1,2)(3,4)(5,0)`). Nine collapse to eight because `(2,3)` is the only pair both adjacent *and* summing to 5 — the **L2/L3 hinge** is Being and Becoming at once, the field's self-inverting middle. The load-bearing finding: **the three lens-squares A/B/C are all the Becoming/mirror family** — one family of three, the complementary-pair slice — so `/mef-refract` fanning "Square B + C" and holding "Square A" was operating *entirely inside the mirror family*, blind to Being (adjacency) and Knowing (crossing). The #0/#5 square is correctly the **Converse-Mirror tetrad on the two implicate poles**, held as the reading's envelope because the poles frame the explicate four — not because it is a "ground." **Amended:** `mef-refract.js` (the `HELD_ENVELOPE` + `FAMILIES` constants; the synthesis now reads convergence through all three registers and holds the #2/#3 hinge double; `SYNTHESIS_SCHEMA` gains a per-position `register` field orthogonal to `relation`/strength), `mef-refract.md` (lens-set by pair-sum, synthesis pass + non-negotiables carry the three registers), `using-epi-logos` (the harmonic-structure section rebuilt: three families, eight squares, the lens-squares as the mirror slice), `converse-pedagogically` (the fuller grammar taught after the three squares), `etymological-archaeology` (the envelope characterization). Backed by data: `resources/canon/ql-musical-derivation-v3.md` (re-added to the ship set — the scaffolder had excluded it) and `data/harmonic-families.json` (the grammar serialized). Naming discipline: harmonic families are named by register (Being/Becoming/Knowing), never "family A/B/C," which would collide with the lens-basin squares. Workflow re-validated: independence still proven, JSON valid. Engine patch still pending (§5): `'Knowing'` → `'Knowing-Unknowing'`, and `grammar-data.js` Reference Table 7 uses the *old* pre-correction B/C swap — build from File Four §2, not Table 7.

**Scaffolding — 2026-07-14.** `resources/` populated (coordinate system, cheat sheet, `mef-12-lenses-sublens-reference.md`, `units/`, `canon/` + the re-added musical derivation, `methods/`, all byte-identical to source), `data/coordinate-system.json` + `determinations.json` + `harmonic-families.json` serialized (values cited), `.claude-plugin/plugin.json` + `marketplace.json` and `README.md` (with the "Dropped, with reasons" roster) created. **Still needs authoring** (reported, not fabricated): `resources/persona/epii.md` (source: §3.3/§3.4 + the `using-epi-logos` inline paradigm), `resources/prompt-package/` (Tier A regen of the legacy trio to current formulations), `resources/essay-okf/` (the OKF canonicalization build, §3.7/§7-step-7).

**Non-negotiables the workflow enforces** (distilled from Files 1–3): run both passes never one alone (T1 count + T0 proportion); honour the §1/0 phase-flip (the observer discovers it is the observed); **preserve the ?/! and the incomputable `1/0` unresolved** — do not patch the point where the system meets its own limit; respect chirality (`0/1` computes, `1/0` does not); know the quilt is provisional (a stitch that claims to be a totalising master-term is the failure); and end with the reader as the proof (close the loop in cognition, not on the page).

**Output: natural chat by default, plate on demand.** The everyday output is natural conversational prose carrying the small lens/status mark (§3.6) — the answer reads like a person talking, with a compact footer showing which lenses and statuses the reasoning touched. The **QL plate** is the heavy, on-demand form: one self-contained HTML template (`templates/ql-plate.html`, no external requests) with the six-position layout, per-claim lens provenance, Derived/Argued/Offered badges, the locked notation, and the dark-serif visual language shared with `sym-dia-ballein-views.html`. Skills render it only for a full reading, an essay plate, or a `mef-refract` convergence — when structure is the point, not an interruption. The essay's eight plates and the plugin's plate are the same design work done once; the plate CSS is a shared token file across surfaces.

**Constraints.** Size under ~500 KB. No absolute paths (grep-enforced). No references to files that don't ship. Installable by a stranger with none of Frank's trees — this is the acceptance test.

---

## 4. Surface 3 — the site component

Ships: the symbol-engine page (`symbol-engine.html` build) + `sym-dia-ballein-views.html` + a short supporting page linking the three surfaces. Deploy target and domain are a build-time decision (no remote or deploy config exists today); the vault (§2) and engine deploy together under one host.

Prerequisites, in order:
1. **Commit the symbol-engine tree** — the entire `src/symbol-engine/` is uncommitted on `poems-as-surfaces`. Nothing else proceeds safely until this is in git.
2. Revise `sym-dia-ballein-views.html` per the central plan's requirement: first view uses the locked full expressions.
3. Static build of the engine page verified standalone (it does not import the main site, so this should be clean).

The whole-site deploy (poems-as-surfaces, main essay site) is explicitly out of scope for the submission and follows at its own pace.

---

## 5. One base, many refractions (not a harmonisation plan)

There is nothing to harmonise: `context/epi_logos_coordinate_system.md` is the base, and each surface refracts it in its own register by analogia (§0). What follows keeps the refractions *faithful*, not identical.

1. **The base ships as data.** The coordinate system's base alignment — the six positions with their questions, QL units, elements, L-links, and the three Klein squares — is the canonical data the plugin carries (`data/coordinate-system.json`, a direct serialisation of the doc's tables, plus the doc itself in `resources/`). Every skill reads from this. This is the bimba.
2. **The engine refracts the same base for its runtime.** A script in `test-site/scripts/` (`export-canon.mjs`) serialises the engine core's grammar (`qlPositions` + `lensRegistry` + `harmonicRelations` + `modes`) for the site's own use. It is verified to match the base (§0), so it is the *computational pratibimba*, not a competing source. Keep it faithful with four patches before it emits shared JSON: Family-C `'Knowing'` → `'Knowing-Unknowing'`; the Pythagorean-comma stub populated or flagged (`531441/524288 ≈ 23.46¢`); the default substrate settled (`canon` drone vs `chromatic` C-major); `'Supramental'` → `'Supermental'`. Grammar only — 144-fold voicing, spectral observer, nine-square, hooks stay runtime.
3. **Faithfulness check, not a concordance-to-identity.** A light check that the engine JSON and the base agree on the six positions × twelve lenses (questions, elements, squares, symmetry partners). Divergence in register is expected and fine; divergence in the *base alignment* is a bug. No prose codegen.
4. **Notation lock** — full expressions `(+1)/(−1)`, `(0/1)/(1/0)` on every surface; the central plan arbitrates.
5. **Naming** — `sym-ballein` in reader-facing notation contexts, per the central plan.
6. **Status badges** — Derived/Argued/Offered rendered identically (vault frontmatter, plate template, essay prose).
7. **Plate style** — one CSS token set shared by the plate template, the vault's embedded plates, and the views page.

---

## 6. What the journal receives at first stage

- Abstract/proposal ≤500 words (rubric-bound prose; written last, when the surfaces exist to be described accurately).
- Author bio, CV, portfolio sample.
- Component description + capacity statement: the vault (essay), the plugin (zip or repo link), the engine + views pages (live URLs) — with a sentence each on what it is and the demonstrated capacity to realise it (they exist; that is the capacity statement).

---

## 7. Build order

1. Commit symbol-engine work in `test-site` (step zero, blocking).
2. Base data: `coordinate-system.json` (serialise the canon doc's tables) + the engine-refraction export → `ql-positions.json` + `mef-lenses.json` + `ql-harmonics.json` (with the four faithfulness patches).
3. Write the epii paradigm (`resources/persona/epii.md`) — the theory of the subject, the #0/#5 envelope, the tone and tool-use instruction, the small-mark output convention — and the `SessionStart` context hook that installs it.
4. Scaffold `submission-package/epi-logos/`; carry the 10 skills with repairs; write `investigate`, `two-logics-of-two`, `okf-wiki`, `walk-the-essay`; plugin.json; README. All skills written to the envelope (§3.5) with the small-mark output default (§3.6).
5. Write `/mef-refract` command + workflow script (fresh-context convergence-as-proof, §3 workflow).
6. Design `ql-plate.html` + shared plate CSS (joint work with the essay's eight plates).
7. **Canonicalise the essay node tree to an OKF bundle** (§3.7): `node_type`→`type`, wikilink→standard-link resolution (OKF Enforcer / `kcmd validate`), generate `index.md`+`log.md`, derive section `coordinates`, promote the five braids to `type: Braid` nodes, add `aperture`/`analogia` frontmatter. Ships in the vault and (snapshot) in `resources/essay-okf/`. This is the bridge the vault and `walk-the-essay` both consume.
8. Regenerate the prompt-package trio (Tier A) to current formulations.
9. Stranger-install test + size/path checks + `kcmd validate` on the bundle + the UX gate (§3.6) on sample runs (acceptance gate for the plugin).
10. Vault publish pipeline (Quartz recommended): the OKF bundle *is* the vault; publish the curated subset with `index.md` as navigation and the braids as traversals.
11. Revise views page (locked expressions first view); static-build engine page; deploy engine + views + vault under one host.
12. Abstract + proposal text (rubric pre-flight + adversarial audit), then submit.

Steps 3–8 are plugin work and can proceed in parallel with 10–11 (vault/site work) after steps 1–2; step 7 (the OKF bundle) is the bridge both depend on.

---

## 8. Testing and acceptance

- **Plugin:** fresh-directory stranger install; each skill smoke-run; `grep` for absolute paths and for references to non-shipped files; size budget check; `/mef-refract` end-to-end on a sample question with the plate output rendered. **UX gate (§3.6):** on sample runs, confirm the response body is natural chat carrying a small well-formed lens/status mark (not a coordinate dump), that the #0/#5 awareness is reflected in the reading even when compressed, and that epii speaks accessibly at a novice level without dropping canon-fidelity — accessibility failures block the same as correctness failures.
- **Persona:** a level-calibration check — the same question posed by a novice and by an expert should draw visibly different apertures (#0) from epii while reaching the same structural reading; and epii should never claim the subject-position (the 0/Ø distinction holds in self-reference).
- **Canon export:** the engine core is already unit-tested; the export script gets a round-trip test (JSON → compare against source objects).
- **OKF bundle:** `kcmd validate` passes; every wikilink resolves (no dangling alias→path); every node carries a `type`; `index.md` reaches every node by traversal; `okf-wiki` refuses to quote a reference whose `verification_status` is unconfirmed (the status gate actually fires).
- **Vault:** spine reads standalone (linear-extraction check); no dead wikilinks in the public subset; no unverified reference note leaks into the publish set.
- **Prose:** abstract and any essay prose pass the writing rubric's full two-pass process.

## 9. Out of scope for the submission

Whole-site deploy; `epi-logos-voice`; tarot/I Ching skills; thought-artifact skills; cross-harness `.codex/`/`.pi-agent/` bundles; prose codegen from JSON; 5-/7-limit substrates, Phase-3 geometry, and `detail:{}` enrichment in the engine; epi-logos.org/about prompt-package hosting (follows later; the vault/engine host can redirect).
