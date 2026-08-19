# Symbolon ↔ O:I Native Wiki / Projection Contract

**Ticket:** 013  
**Status:** complete affected-field contract for global Pass B; no O:I product implementation performed here  
**Source field:** `CANONICAL-FIELD-CENSUS.md` + `PROTOCOL-RECONCILIATION.md`  
**Technical evidence boundary:** revalidated `SOURCE-AND-AUTHORITY-MAP.md`; O:I founding/co-internality/product-field contracts; AIKit `okf-wiki/v1`, `KnowledgeApplication` and `KnowledgeOperations` at the pinned head.

## 0. Contract in one sentence

**Symbolon remains the canonical authored knowledge world; O:I exposes a selective, provenance-bearing Projection of that world; AIKit makes the Projection and its native sources navigable without translating them into a second ontology; any change produced through encounter remains a Projection revision or source-return proposal until the canonical source explicitly accepts it.**

The important consequence is that publication, projection, navigation, contribution and learning are five different relations. No amount of convenience at the O:I surface is allowed to collapse them.

---

# 1. The older relation this contract must preserve

The Wiki contract does not begin from database objects.

A Symbolon record is a determinate authored mark inside a relation it does not exhaust. Its identity carries a source/home, its written links state how it is implicated with other determinations, and its Return states where the record becomes answerable beyond itself.

That architecture is already the dia/sym-ballein engine in publication form:

- **dia-ballein** makes distinct records, claims, registers, sources and operations explicit;
- **sym-ballein** preserves the relation among the differentiated records through written links, provenance and Return;
- **counterfeit gathering** occurs when an index, renderer, learned graph or product representation presents its compilation as if it were the authored whole;
- **Return** is the explicit route by which encountered difference can pressure the authored source without silently becoming it.

O:I and AIKit therefore have a constrained job: make the relation more traversable and encounterable **without taking the zero-position of the source world**.

---

# 2. Canonical source identity and one-home law

Every ratified Symbolon record has exactly one canonical authored source identity/home in this repository.

A canonical identity is not its rendered URL, database row, search index identifier, AIKit provider identifier or O:I Wiki node id. Those are address/projection mechanisms.

The minimum source identity is:

```text
repository = EpiLogos/Antykathera-Essay-Work
canonical_path = <ratified repository-relative path>
canonical_revision = <git revision or accepted source revision>
record_identity = <stable source-relative identity>
```

For the post-ratification build, `record_identity` should remain stable across a file rename only where an explicit migration/alias record says that the same authored record moved. A merge or split creates an explicit lineage relation; it must not be disguised as a filename move.

**One home does not mean one representation.** The same source record may appear in:

- the raw repository;
- a generated local room;
- an O:I WikiSpace;
- LIST/TREE/GRAPH navigation;
- an agent Knowledge reading;
- a submission-site rendering;
- a bounded exported corpus.

Those presentations all point back to the one canonical source identity.

---

# 3. Register and `record_type` remain independent

O:I/AIKit must not infer a new ontology from directory shape.

Symbolon preserves at least these publication registers:

```text
Symbolon root
Matheme
Mytheme
Episteme
```

and linear argument records remain a distinct section-room publication office consuming those registers.

`register` answers **how this record knows/performs**. `record_type` answers **what kind of publication object it is**.

Examples:

- Matheme + `derivation`
- Matheme + `formal-neighbour`
- Mytheme + `poem`
- Mytheme + `myth`
- Mytheme + `plate`
- Episteme + `concept`
- Episteme + `history`
- Episteme + `etymology`
- Episteme + `dossier`
- Episteme + `figure`
- Episteme + `dialogue`
- Episteme + `map`
- Episteme + `source-facing-record`
- Symbolon + `root-relation`

No fixed inventory count belongs in the contract. The ratified census determines which records actually exist.

AIKit's current `okf-wiki/v1` is compatible with this law because its `WikiNode.node_type` is an open string and unknown extension fields are retained rather than translated into AIKit-owned kinds. The adapter should therefore **carry** Symbolon's register/type semantics, not replace them.

---

# 4. Raw QL page structure is source semantics

Every developed field page begins from the source chassis:

```markdown
# <record title>

## #0

## #1

## #2

## #3

## #4

## #5→0
```

The six positions have no universal semantic gloss.

A renderer may present six positions visually. AIKit's current Wiki constellation support can even preserve numeric positions `0..5` and explicit return paths. But neither AIKit nor O:I may infer:

```text
#0 = ground
#1 = definition
#2 = operation
#3 = pattern
#4 = context
#5 = quintessence
```

or any other global table.

For a particular source page, a subtitle such as `## #2 — The cut becomes a selection field` may be authored because that local record earned it. The renderer may display that subtitle; it must not generalise it across unrelated records.

### QL structural metadata

Where useful, a Projection may expose:

```text
ql_positions:
  - source_anchor: #0
    local_label: <optional authored subtitle>
  ...
return_anchor: #5→0
```

But the body and authored heading remain the authority. Generated structural metadata is subordinate and reproducible.

---

# 5. Minimum canonical source metadata

A developed record must be able to project the following without requiring those fields to be embedded in one universal frontmatter format if the repository already has an equivalent canonical representation:

```text
record_identity
canonical_path
canonical_revision
register
record_type
publication_office
claim_state
source_authority
source_refs[]
citation_state
quotation_state
relations[]
return_targets[]
aliases / lineage where applicable
selection_state for public Projection
```

## 5.1 Claim state

Claim state remains typed. At minimum the field must distinguish situations equivalent to:

- Authored/Argued — an essay proposition whose warrant is the argument itself;
- Derived — follows from stated formal premises/operations;
- Sourced — report of an external source with adequate citation support;
- Offered/Research — proposed correspondence or programme not yet independently established;
- Open — explicitly unresolved question/debt.

The exact existing vocabulary is retained rather than renamed merely to fit O:I.

## 5.2 Source authority

Source authority is question-sensitive.

- Symbolon source is authoritative for the authored record and its accepted wording/relations.
- A cited book/paper is authoritative only for claims it actually supports.
- O:I product documentation is authoritative for O:I intent/accepted architecture at its revision.
- implementation/code/tests are authoritative for implemented behaviour at their revision.
- an AI-generated explanation is a derived reading, not source authority.

A Projection therefore carries source authority rather than manufacturing it.

## 5.3 Citation / quotation readiness

A record can be structurally canonical while a source debt remains Open. The Projection should be able to expose citation/quotation readiness so an agent or human can distinguish:

- safe to quote/source now;
- source identified but page/edition verification outstanding;
- role is comparative/background only;
- internal authorial material, not external warrant.

Open debt is visible status, not silent deletion.

---

# 6. Written relations are the authored graph

A Symbolon relation exists canonically because it is written and attributable in the source field, not because two pages share vocabulary or an embedding score.

Current declared relation vocabulary includes:

```text
derives
grounds
defines
historicises
sources
qualifies
tests
figures
embodies
extends
compares
presages
returns-to
```

T07/T23 may ratify additions where the field requires them. No numeric degree quota applies.

A projected Wiki edge must preserve at least:

```text
from_record_identity
to_record_identity
relation
origin = authored | mechanical | compiled | inferred | learned | QL-derived | MEF-derived
origin_ref / source anchor when applicable
revision
```

This maps cleanly onto AIKit's current `WikiEdge` and `WikiEdgeOrigin` distinction.

### 6.1 Authored edge ≠ inferred edge

An inferred/learned edge may be useful for discovery, but it never becomes a canonical relation merely because a model or graph algorithm found it.

The human interface should visually distinguish:

- authored relation;
- mechanically compiled inverse/navigation edge;
- QL/MEF-derived reading;
- inferred/learned suggestion.

The agent interface must expose the same distinction in structured data.

### 6.2 Block-level anchors

Where the relation depends on a specific claim, the edge should preserve the existing exact block/heading anchor rather than degrading to a page-level association. This is especially important for source claims, claim-status changes and return points.

---

# 7. Return is not a backlink

A backlink says “another record points here.” Return says **where the operation becomes answerable**.

A record's Return may point to:

- an earlier ground/root relation;
- a source owner;
- a linear argument that consumes the radial record;
- a different register that constrains the claim;
- a human/Project authority locus;
- an empirical experiment/evidence requirement;
- an O:I Projection return proposal;
- a terminal `/0` relation.

A projected Wiki must therefore preserve explicit `return_targets`, not infer Return from inbound links.

AIKit's current `WikiConstellationReturn` can represent a return path through an anchor into a ground reference for constellation-shaped readings. That is useful infrastructure, but it does not define Symbolon's meaning of Return. The source relation remains authoritative.

---

# 8. Source, WikiSpace, Projection, Context and SharedField

These are deliberately different objects/relations.

## 8.1 Source

The canonical authored record(s) in this repository. Source owns accepted wording, identity, source relations and authored edge state.

## 8.2 Projection

A selective representation of source for an O:I purpose/surface. It has its own projection identity and revision and retains a pointer to the source identity/revision from which it was formed.

Projection may:

- select a subset of the source world;
- add rendering/layout state;
- compile navigation;
- expose source metadata;
- carry proposed edits/annotations;
- diverge intentionally.

Projection may **not** silently redefine source.

## 8.3 WikiSpace

An addressable knowledge space containing projected Wiki objects. A WikiSpace can organise/relate records for traversal. It is not automatically the source filesystem and it is not the whole SharedField.

AIKit `okf-wiki/v1` supplies a real current representation for WikiSpace/Node/Edge/Frame/Reading with revision/provenance while preserving native ontology.

## 8.4 Context

The smaller operative information field disclosed to an actor for a particular act. AIKit explicitly distinguishes existence/availability/selection/projection/loading/invocation. A Wiki record can be addressable without entering standing context.

Therefore:

> `SharedField ≠ WikiSpace ≠ Context`.

## 8.5 SharedField

The wider O:I relational field in which independently grounded worlds may encounter/contribute/relate. A Symbolon WikiSpace may participate in SharedField without SharedField becoming the canonical Symbolon store.

---

# 9. Projection identity and revision model

The minimum Projection contract is:

```text
projection_ref
projection_revision
source_world_ref
source_revision
selection_spec
projected_record_refs[]
projection_state
provenance[]
parent_projection_revision? 
divergence_state
```

### Projection states

A useful minimal state machine is:

```text
source-bound
    selective representation of one accepted source revision

projection-revised
    edits/annotations/relations exist in Projection only

return-proposed
    one or more Projection changes are packaged as explicit source-return proposal

accepted-to-source
    source owner accepted the proposed change through the source's normal process;
    new source revision now exists, and a fresh Projection can bind to it

divergent
    Projection intentionally retains a different line; source is unchanged
```

No “synced” status should imply that bidirectional database mutation can bypass source acceptance.

---

# 10. Source → Projection → encounter → Return state machine

The complete state machine is:

```text
canonical Symbolon source
        │
        │ selective Projection with source revision/provenance
        ▼
O:I WikiSpace / Explore
        │
        ├── read / navigate / render
        ├── encounter
        ├── annotate
        ├── propose relation
        ├── propose edit
        └── derive reading
        │
        ▼
Projection revision
        │
        ├── remain Projection-local
        ├── intentionally diverge
        └── package source-return proposal
                    │
                    ▼
          explicit source review/acceptance
                    │
             ┌──────┴──────┐
             ▼             ▼
       accepted change   rejected/unaccepted
             │             │
             ▼             ▼
       new canonical     Projection remains
       source revision   distinct/divergent
             │
             └──────→ regenerate/rebase Projection if desired
```

The critical law is **explicit acceptance to source OR divergent Projection**. There is no hidden third path in which a browser edit simply becomes canon because it occurred in the “same wiki.”

---

# 11. Contribution, Wiki relation and learned route are distinct

O:I must preserve at least three relations that conventional wiki systems often flatten.

## Wiki relation

A semantic relation among projected/source knowledge records. It carries relation type and origin.

## Contribution relation

An event/object entering SharedField under provenance/admission/authority rules. A contribution may propose text, data, evidence, code or another object. It does not become a Wiki edge merely by being adjacent to a record.

## KnowledgeRoute

AIKit's operational traversal record: how a query/actor moved across providers/addresses. The current implementation explicitly says route records traversal and **does not mutate provider graphs**.

Therefore:

> `Wiki relation ≠ Contribution relation ≠ learned KnowledgeRoute`.

Learned familiarity may make a destination easier to reach; it must not become trust, authored preference or canonical relation without an explicit conversion act.

---

# 12. Actual AIKit seams to reuse

The contract binds to the implemented primitives verified at `EpiLogos/ai-kit@42127820d6e5bf4ea5ee248e88e305e14c5c1a7c`.

## 12.1 `okf-wiki/v1`

Current portable semantic objects:

- `WikiSpace`
- `WikiNode`
- `WikiEdge`
- `WikiFrame`
- `WikiReading`
- provenance refs and semantic revisions
- open node type / extension fields
- authored/mechanical/compiled/inferred/learned/QL-derived/MEF-derived edge origins
- Wiki constellations and explicit return paths.

This is a strong fit because provider/index/database identifiers are forbidden from defining canonical Wiki identity and project ontology stays open.

## 12.2 `KnowledgeApplication`

The current application is explicitly **federation, not a universal graph**. It can bind:

- Semantic Wiki provider;
- SourcePool providers;
- code index;
- ProjectMap federation.

The provider keeps its own relation/ranking/identity semantics. That matches Symbolon's one-home/source-authority law.

## 12.3 `KnowledgeOperations`

The canonical current operation vocabulary is:

```text
search
read
relations
route
frame
sources
explain
history
status
```

`frame` is a derived context-pack projection, deliberately not a canonical ContextSource. `route` does not mutate graphs. `sources` exposes provider-owned provenance. These are exactly the distinctions the Symbolon field needs.

## 12.4 ProjectCentral / Central relation

Current AIKit/Central work lets locally authored Wiki worlds enter Knowledge Navigation while keeping filesystem/source identity and provenance with Central/Project source. Symbolon should use the same architectural principle even though this essay repository, not Central, is its canonical source owner.

## 12.5 AIKit “projection” naming collision

AIKit also contains a `projection.rs` concerned with projecting effective capability views into client targets. That is a different operation from O:I authored-world `Projection`.

Do not merge the types merely because they share the English word. If code integration requires both in one namespace, names should make the distinction explicit, e.g. `TargetProjection` versus `KnowledgeProjection`/`WorldProjection`.

---

# 13. Higher-order praxis names: current evidence status

The 013 ticket names:

- `product-understanding`;
- `structured-account-authoring`;
- `projection-authoring`.

At the revalidated AIKit head, those literal names were **not established by repository search as accepted implemented Skills**. The contract therefore does not falsely depend on them.

Their intended operations are nevertheless real and can be supplied through existing primitives or explicit future Skills:

### Product-understanding role

Provenance-aware traversal across source, design, architecture, implementation, evidence and returned findings.

**Current primitives:** Knowledge `sources/read/relations/route/explain/history` + ProjectMap/SourcePool/Wiki federation.

### Structured-account-authoring role

Build a coherent account from selected records while preserving source authority, relation origin, divergence and claim status.

**Current primitives:** Wiki frames/readings + Knowledge routes/frames/sources.  
**Missing higher-order product feature:** an explicit authoring procedure that packages its selected evidence/relations and makes the account's derived status unavoidable.

### Projection-authoring role

Select source records into an O:I Projection, revise the Projection, and return proposed changes toward source.

**Current primitives:** source/Wiki identity, semantic revisions/provenance, reading/navigation.  
**Missing product feature:** source-aware Projection revision + return-proposal/acceptance workflow as specified here.

If those Skill names later land as accepted implementations, they can implement this contract; the contract does not predeclare them implemented.

---

# 14. Human and agent readings share identity

Humans and agents should not receive two semantic worlds.

A human may see rich rendered Markdown, diagrams, provenance cards and graph traversal. An agent may use structured Wiki/Knowledge operations. Both must resolve the same:

- source record identity;
- source revision;
- relation type/origin;
- claim/source status;
- QL local structure;
- return target;
- Projection revision.

Agents should not be required to scrape rendered HTML to recover semantics that already exist structurally. Humans should not be shown a graph whose important relation-origin/source distinctions disappear because the structured model is richer than the UI.

### Minimum human views

- **READ** — authored page/argument with source/projection status visible.
- **LIST** — selected records grouped by register/type without turning group into ontology.
- **TREE** — source or curated hierarchical navigation where a hierarchy is actually authored/declared.
- **GRAPH** — authored relations first; inferred/learned layers toggleable and visually distinct.
- **PROVENANCE** — source, claim/citation status, projection revision, returned proposals.

### Minimum agent access

- direct `read` of canonical projected address;
- `relations` with origin/source metadata;
- `sources` / `explain`;
- `route` / `history` without graph mutation;
- ability to request deeper Matheme/Mytheme/Episteme records by stable identity;
- explicit absence/degradation rather than fabricated context.

---

# 15. The authority/operation ladder

A useful traversal can be exposed without turning it into a universal hierarchy:

```text
authored position / root relation
        ↓
principle / argument / constitutional intent
        ↓
design relation / product responsibility
        ↓
architecture / contract / operation
        ↓
implementation / experiment / evidence
        ↓
finding / critique / returned pressure
        ↺
explicit proposal back toward authored ground
```

The direction does not mean that source is always factually superior. It means authority is **role-sensitive**.

For example:

- essay source owns the proposition “dia/sym-ballein is a foundational relation in this authored system”;
- AIKit source owns whether `KnowledgeOperations::route` mutates provider graphs;
- an experiment owns its measured result;
- returned implementation evidence may falsify a software correspondence and pressure the authored account;
- none of those facts lets implementation silently rewrite the essay source.

O:I Explore should make this ladder inspectable as provenance, not flatten everything into “related pages.”

---

# 16. Native relation from essay concept to O:I/product/research surfaces

The essay becomes genuinely useful as an O:I world when a concept can be traversed **outward to its technical realisations and back**.

Example:

```text
Dia/Sym-ballein (root + argument)
      ↓ grounds / compares
Objective Internality
      ↓ operationalises / tests
Actuation Return
AIKit source/context disclosure
Factory Recognition
Workcell observed material evidence
QL Operational Parity
      ↓ returns-to
Power / Co-Internality / Return of Zero
```

The product nodes are not copied into Symbolon as new ontology. A source-facing technical dossier/map records:

- product/responsibility identity;
- exact source revision;
- claim role: intent / accepted architecture / implementation / experiment;
- relation to essay operation;
- source link/provenance;
- last verified date;
- known open/development boundary.

That creates a first-class research bridge without making the essay repository an outdated mirror of seven codebases.

---

# 17. Publication and selection boundary

Not every developed source record must be public in every Projection.

A Projection selection can include:

```text
public linear argument
public radial depth
private/internal working evidence
source-debt state
technical research records
submission-only supporting material
```

Selection is explicit. Omission from one Projection is not deletion from source.

Likewise, a public Explore world can expose deep Matheme/Mytheme/Episteme traversal without forcing all radial material into the sovereign manuscript. This is the practical expression of the census law: **publication depth ≠ manuscript burden**.

---

# 18. Product requirements versus essay-repository requirements

## 18.1 Essay repository requirements

These belong here and should be completed through T07–T24:

- ratify final record identities/offices;
- develop pages with raw QL/local semantics;
- make one-home/register/type/claim/source state explicit enough to compile;
- write actual relations and returns;
- preserve block anchors where needed;
- maintain source revision/provenance for technical dossiers;
- produce a deterministic projection manifest or equivalent source-readable export after the canonical field exists;
- maintain public-selection state without deleting non-public source records.

## 18.2 O:I / AIKit product requirements

These are downstream product features; **do not implement them in this essay ticket**:

1. **Source-aware world Projection identity.** Represent source world/revision, selection spec and Projection revision independently from Wiki object ids.
2. **Projection revision workflow.** Browser/Explore edits remain Projection-local until explicit return.
3. **Source-return proposal object.** Package proposed source edits/relations with base revision, provenance, author/agent identity and conflicts.
4. **Explicit acceptance/divergence.** Source owner can accept into source or leave/reject as divergent Projection.
5. **Relation-origin rendering.** Human graph/read views distinguish authored/mechanical/inferred/learned/QL/MEF edges.
6. **Authority-layer traversal.** Expose source/intent/design/implementation/evidence/finding relations without asserting one global authority order.
7. **Claim/citation state rendering.** Open source debt and role-sensitive evidence visible to humans and agents.
8. **Stable deep links.** Same record/anchor identity resolves across READ/LIST/TREE/GRAPH and agent Knowledge operations.
9. **Projection/source provenance receipt.** Sufficient for acceptance: source repo/revision, projection revision, selection, compiler/version, relation counts by origin, unresolved links/debts.
10. **No semantic use of renderer-specific QL position glosses.** The renderer may show local authored subtitles only.

The current AIKit Knowledge/Wiki primitives satisfy much of the read/navigation/provenance floor. The authoring/return loop is the principal missing higher-order capability named by this contract.

---

# 19. First genuine O:I authored-world acceptance shape

After T24, *The Return of Zero* can serve as an O:I acceptance world if the following can be demonstrated from one source revision:

1. load/select canonical Symbolon source without changing it;
2. create one Projection identity tied to that source revision;
3. expose the linear essay/argument route plus bounded local whole;
4. traverse LIST/TREE/GRAPH from the same authored relations;
5. move from an argument into Matheme/Mytheme/Episteme and back through explicit Return;
6. inspect relation origin and source/claim authority;
7. query the same world through agent Knowledge operations;
8. create a Projection-local edit/annotation or proposed relation;
9. package that difference as a source-return proposal;
10. show that source is unchanged until explicit acceptance;
11. either accept to a new source revision or retain a visibly divergent Projection;
12. emit a provenance receipt proving the relation.

That acceptance is far stronger than “render the repo as a wiki.” It demonstrates Objective Co-Internality in miniature: an authored source world and a projected operative world can affect one another without either silently becoming the other.

---

# 20. Affected-field recheck against `CANONICAL-FIELD-CENSUS.md`

## 20.1 Root pressure

**No new root is required.** The contract strengthens the five Pass-A roots:

- `0/1` — source/ground → determination orientation;
- `1/0` — determination → ground/Return orientation;
- `/` — relation/means/cut;
- Dia/Sym-ballein — explicit differentiation + retained/recomposed relation;
- Mono/Poly — one/many relation.

Source/Projection is a powerful technical/cognitive relation but does **not** need to become a sixth universal Symbolon root. It is adequately grounded by slash + dia/sym + Bimba–Pratibimba + Co-Internality.

## 20.2 Concept pressure

The contract confirms these Pass-A concepts:

- Bimba–Pratibimba;
- Objective Co-Internality;
- Positional Ground;
- Protected Account;
- Register Grammar;
- MEF;
- World-Picture→World-Atlas;
- Counterfeit Symbolon.

**Projection** should not become a generic standalone Episteme concept page unless 014 finds conceptual work beyond Bimba–Pratibimba/O:I source contract. At present it is better carried as a relation inside those records plus the technical dossier.

## 20.3 Episteme pressure

A developed **O:I / technical responsibility and source-projection dossier/map** is definitely required after ratification. Its role is not to document every product. It preserves:

- exact responsibility centre;
- current evidence revision;
- intent/architecture/implementation/research status;
- relation back to the relevant essay operation;
- source/projection/authority boundary.

AIKit Knowledge/Wiki itself belongs in that dossier as an implementation-facing witness, not as a new Symbolon register.

A second distinct Episteme record is likely required for **source / projection / contribution / route distinctions** if the technical dossier becomes too broad. 014 must test whether that deserves a concept/dossier split.

## 20.4 Path pressure

The contract does not itself justify a new navigation path. T23 should first see whether authored links plus the O:I technical dossier let a reader traverse source→Projection→encounter→Return without a curated path. If not, a single `Symbolon source → O:I Projection → source Return` path is warranted.

## 20.5 Duplicate pressure removed

The one-home + Projection model explicitly removes the need for:

- duplicate “O:I versions” of Symbolon concepts;
- AIKit-owned translations of Matheme/Mytheme/Episteme types;
- separate human and agent graph ontologies;
- inferred relations copied into authored Markdown as if canonical;
- browser-edited copies pretending to be source;
- QL-renamed copies of native O:I objects.

## 20.6 Global Pass-B questions for 014

014 must test:

- whether the source/projection distinction deserves a standalone Episteme dossier versus living inside the technical responsibility dossier;
- whether Counterfeit Symbolon is best as a canonical concept or a section within provenance/trust;
- whether existing Bimba–Pratibimba wording is strong enough to carry Original/source/projection without a second concept;
- whether one or two transverse navigation paths remain necessary after all written relations are propagated;
- whether any old map/path now duplicates the explicit Wiki/source contract and should be merged/rehome with named carrier.

No canonical source page is altered by 013.

---

# 21. Contract result

The contract makes the essay's knowledge architecture and O:I's technical architecture homologous **without pretending they are identical**.

Symbolon remains authored source. A Projection is an avowed pratibimba: selected, revisable, useful and non-sovereign. WikiSpace makes that projection addressable. AIKit federates it with sources/code/project knowledge without becoming a universal graph. Context remains the smaller disclosed field for an act. SharedField remains the wider field of encounter/contribution. Learned routes remain learned routes. Return remains an explicit proposal back to source authority.

The publication architecture therefore preserves the same foundational law as the argument:

> **Dia differentiates source, projection, context, contribution and reading. Sym keeps their relations explicit. Return lets encountered difference pressure the source without counterfeit gathering—without the Projection pretending it was the Original all along.**
