# Adaptive Pasu encounter and compilation — decision brief

Prepared: 2026-08-01 (Europe/London)  
Status: preparation for the open HITL ticket; this document does not resolve or close the ticket

## Recommendation in one sentence

Build the encounter as a resumable six-movement conversation—an opening `#0` frame, exactly four primary questions, and an open `#5` return frame—whose turns become an evidence-bearing source form and attractor-basin candidate before the existing mapper compiles the full `6+6′`; the conversation may leave canonical positions missing, unknown, conflicted, or withheld, and it must never ask extra questions merely to make the twelve-position frame appear complete.

The user-facing encounter should contain no QL vocabulary. `Pasu`, `QL`, `Bimba`, `Pratibimba`, position names, occupancy states, evidence registers, basin language, and compiler accounting remain internal. The person sees one brief frame or image of thought, one question at a time, and a final return which recognises what moved without claiming to explain or finish it.

## Governing constraints recovered

This brief follows the existing product and project contracts rather than replacing them:

- The full card contains exactly `P0…P5` and `P0′…P5′`, followed by the enriched `P5′→P0⁺` return. `P0⁺` is not a thirteenth position.
- Threshold `0/1` binds the Pasu snapshot, session, exact temporal snapshot, attractor and basin, intention, source material, permissions, lens, and profile set.
- The QL mapper reads native source form before allocation, preserves exclusions and unresolved material, and records explicit occupancy: `present`, `latent`, `missing`, `unknown`, `withheld`, `conflicted`, or `overdetermined`.
- A source member may be distributed across several positions, several source members may be condensed into one position, and some members may remain globally unassigned. No turn-to-position bijection is licensed.
- A final frame may be structurally complete while semantically incomplete. Unsupported content stays absent or receives an explicitly bounded extension register; the mapper does not generate claims to fill empty display space.
- The native QL field moves from ground, through answerable definition, force, recurrence, personed context, and differential horizon, then returns through the incomputable ground. The encounter uses this movement to shape attention, not as a questionnaire whose six labels are exposed or mechanically asked in order.
- Relevant memory belongs to objective-internal context. It may condition a question only through a selected, immutable, consented projection. Opaque harness memory is never canonical state.
- Private, shared, public, and provider-facing uses are separate projections. Permission to use a detail in the local encounter does not imply permission to publish it or send it to an external media provider.
- The encounter's presentation `#0` and `#5` are movements of the conversational form. They must not be copied automatically into canonical `P0` and `P5`, and the `#5` frame is not the final `return.deposit` record. Compilation must establish those later relations through evidence and validation.

## Product behaviour

### The six presentation movements

| Movement | Visible behaviour | Internal work |
|---|---|---|
| Opening `#0` | A very short poem, paradox, field of words/concepts, or symbol-in-transformation, followed by the first plain question. | Gathers the initial prompt and permitted context into an open field. It discloses attention without announcing a diagnosis. |
| Primary question 1 | One natural question about what is presently appearing or attracting attention. | Begins native-form collection. It does not target `P1` as a database slot. |
| Primary question 2 | One natural continuation shaped by the first answer. | Seeks the live quality, pressure, value, feeling, image, memory, or desire that has become available. |
| Primary question 3 | One natural continuation shaped by the accumulated exchange. | Seeks movement, relation, gesture, passage, change, obstruction, or recurrence where it is live. |
| Primary question 4 | One natural continuation which situates what has emerged and permits a boundary or withholding. | Seeks contact with present life, desired form, implication, limit, or what must remain unnamed. |
| Return `#5` | A concise poem, paradox, word/concept field, or transforming symbol which gathers the encounter and leaves an opening. | Produces a proposed return articulation and compiler seed. It does not claim completion, certainty, or possession of the Pasu. |

The descriptions of questions 1–4 state a default movement, not four hidden form fields. The selector may reorder or braid them. A response can bear material for several QL positions and their conjugates; a position can draw from several responses, the initial prompt, approved context, or a declared source. No primary question is generated because an internal position counter says “empty.”

### Four-primary-question invariant

An encounter contains exactly four `primary` question records. Each reaches one terminal response state:

```text
answered | skipped | withheld | abandoned_by_user
```

`skipped` and `withheld` count toward the four-question limit. They preserve agency and become semantic evidence about absence or boundary; they never authorise an inferred answer.

Clarifications are separate records. They do not increment or replace the primary-question count. A clarification is permitted only when one of these conditions holds:

1. an essential referent is genuinely ambiguous;
2. a new sensitive detail appears and its allowed use is unclear;
3. two live statements conflict in a way that changes the intended object;
4. the Pasu asks for clarification or correction;
5. a response cannot be represented safely without knowing what must remain unnamed.

Brevity alone is not grounds for clarification. “Communication, beauty and connective creativity” is a valid answer. The engine must not turn spare language into an interrogation, and it must not ask a clarification whose real purpose is to populate a QL position.

### Natural-language constraints

Every primary or clarification question must pass deterministic presentation checks before display:

- addresses the person as `you` or uses an equally direct natural form;
- contains one main interrogative movement;
- uses the person's own concrete words where doing so is permitted and not merely repetitive;
- contains no internal vocabulary (`Pasu`, `QL`, position address, basin, occupancy, Bimba, Pratibimba, conjugate, mapping, audit, lens);
- contains no diagnosis or identity claim about the person;
- does not reveal that private memory exists when the selected context projection excludes it;
- does not presuppose an interpretation the person has not supplied;
- offers no forced multiple-choice ontology unless the person asks for options;
- does not ask for information already present in the current immutable encounter projection or transcript;
- remains answerable in one phrase, though longer answers are welcome.

Length should be a profile rule, not a metaphysical constant. A useful v1 default is one sentence and no more than 28 words, with an exception only when a short quoted phrase from the Pasu is needed for clarity.

## Production runtime state machine

### Aggregate

The encounter needs a first-class persisted aggregate. It cannot be complete only in a browser component or an opaque chat history, because the same encounter must resume in another harness and compile into evidence-bearing state.

Recommended aggregate identity:

```text
encounter_id
engagement_id
session_ids[]
encounter_version
status
context_projection_id + context_projection_hash
initial_prompt_source_member_id
presentation_profile_id + version
dialogue_policy_id + version
compiler_profile_id + version
primary_question_count
active_primary_question_id?
opening_frame_revision_id?
return_frame_revision_id?
compiled_source_form_id?
compiled_basin_revision_id?
compiled_ql_frame_revision_id?
created_at / updated_at / completed_at?
```

The engagement and attractor may begin as provisional local records. Their approved identity does not depend on a Bimba map or an external graph.

### States and transitions

```text
created
  → awaiting_context_consent
  → context_frozen
  → opening_ready
  → awaiting_primary_answer
       ↔ awaiting_clarification
       ↔ paused
       → awaiting_primary_answer       # next primary, while count < 4
       → return_ready                  # once four primaries are terminal
  → awaiting_return_disposition?       # pending Frank's decision below
  → compiling
  → awaiting_semantic_review
  → compiled_candidate
  → approved

Any non-terminal state → cancelled
context or answer revision → superseding encounter version → earliest affected state
consent revocation → redaction/reprojection → invalidated or cancelled
compiler failure → failed_retryable | failed_terminal
```

#### State invariants

| State | Required invariant |
|---|---|
| `created` | Session identity exists; no memory has been exposed. |
| `awaiting_context_consent` | Candidate context may be named generically for consent, but its content cannot influence generated language. |
| `context_frozen` | An immutable encounter-local projection records included and redacted paths, source revisions, allowed purposes, receipt, and hash. |
| `opening_ready` | Opening frame records mode, text, support references, profile/model receipt, and presentation checks. |
| `awaiting_primary_answer` | Exactly one active primary question exists; count is `0…4`; prior turns are immutable within this encounter version. |
| `awaiting_clarification` | Clarification refers to one prior turn and an allowed reason; primary count is unchanged. |
| `return_ready` | Exactly four primaries are terminal; the return frame is generated only from permitted source members and marked as a proposal. |
| `compiling` | Transcript source form and context projection are frozen by hash; concurrent edits cause conflict rather than silent recompilation. |
| `awaiting_semantic_review` | Candidate basin and full twelve-position QL revision exist; blocking validation findings are visible. |
| `compiled_candidate` | Structural validation passes; incompleteness and all extensions are explicit; the frame is not approved merely because compilation finished. |
| `approved` | Existing `ql.approve` requirements are satisfied by an authorised actor. |

Pause and resume must round-trip through SQL. Replaying the same response with the same idempotency key returns the same turn and does not generate a fifth primary question.

### Action-surface gap

The present 66-action catalogue has no action capable of persisting an encounter turn or updating `epi_session.resumable_state`. Keeping the dialogue only in harness memory would violate the runtime's own portability and shared-action commitments.

The cleanest implementation is a single versioned action, tentatively `encounter.advance`, whose `operation` is `begin | answer | clarify | skip | withhold | revise | return_disposition | cancel`. The action owns state transition, event persistence, idempotency, generation receipt, and response. `session.resume` can expose the active encounter summary without mutation. Compilation then invokes the existing `source.ingest`, `basin.resolve`, `ql.initialize`, `ql.map`, `ql.reconcile`, and `ql.validate` actions.

Adopting this recommendation requires a versioned change to the action registry and acceptance assertion which currently expects exactly 66 rows. The alternative—expanding an existing action's semantic contract—would be a disguised breaking change and is not recommended. This is an engineering contract decision still to be recorded; the brief does not silently change the catalogue.

## Typed encounter contract

The following language-neutral TypeScript notation gives the required shape. UUIDs, timestamps, profile references, hashes, and action envelopes use the existing Epi-Card definitions.

```ts
type Disclosure = "secret" | "private" | "shared" | "public";
type Purpose =
  | "encounter_read"
  | "semantic_compilation"
  | "provider_generation"
  | "public_card"
  | "package_export";

type FrameMode =
  | "poem"
  | "paradox"
  | "word_field"
  | "concept_field"
  | "symbol_transformation";

type QuestionKind = "primary" | "clarification";
type PrimaryDisposition =
  | "answered"
  | "skipped"
  | "withheld"
  | "abandoned_by_user";

type ClarificationReason =
  | "ambiguous_referent"
  | "consent_boundary"
  | "material_conflict"
  | "user_requested"
  | "withholding_boundary";

interface ContextCandidate {
  context_item_id: string;
  source_kind:
    | "initial_prompt"
    | "pasu_attribute"
    | "prior_engagement"
    | "current_session"
    | "user_supplied_source";
  source_id: string;
  source_revision: string;
  label_for_consent: string;
  disclosure: Disclosure;
  valid_at: string;
  relevance_reason: string;
  requested_purposes: Purpose[];
  external_provider_ok: boolean;
}

interface ContextPermission {
  context_item_id: string;
  allowed_purposes: Purpose[];
  decision: "allow" | "deny" | "allow_redacted";
  redacted_paths: string[];
}

interface EncounterContextProjection {
  projection_id: string;
  projection_version: number;
  pasu_snapshot_id: string | null;
  source_revision_manifest: Record<string, string>;
  included_items: Array<{
    context_item_id: string;
    included_paths: string[];
    permitted_purposes: Purpose[];
  }>;
  redacted_items: Array<{
    context_item_id: string;
    redacted_paths: string[];
    reason: string;
  }>;
  consent_receipt_id: string;
  snapshot_hash: string;
  created_at: string;
}

interface EncounterBeginInput {
  session_id: string;
  engagement_id: string;
  initial_prompt: string;
  initial_prompt_disclosure: Disclosure;
  temporal_snapshot_id: string | null;
  context_permissions: ContextPermission[];
  presentation_profile: { id: string; version: string };
  dialogue_policy: { id: string; version: string };
  compiler_profile: { id: string; version: string };
  locale: string | null;
}

interface EncounterFrame {
  frame_id: string;
  encounter_version: number;
  movement: "opening_0" | "return_5";
  mode: FrameMode;
  text: string;
  support_source_member_ids: string[];
  context_item_ids: string[];
  offered_extension_ids: string[];
  presentation_check_id: string;
  generation_receipt_id: string;
  disclosure: Disclosure;
}

interface EncounterQuestion {
  question_id: string;
  encounter_version: number;
  kind: QuestionKind;
  primary_index: 1 | 2 | 3 | 4 | null;
  text: string;
  follows_turn_ids: string[];
  context_item_ids: string[];
  internal_facets: CoverageFacet[];
  clarification_reason: ClarificationReason | null;
  presentation_check_id: string;
  generation_receipt_id: string;
}

type CoverageFacet =
  | "appearing_centre"
  | "felt_quality"
  | "value_or_desire"
  | "relation_or_gesture"
  | "movement_or_change"
  | "pattern_or_recurrence"
  | "situated_contact"
  | "obstruction_or_cost"
  | "desired_expression"
  | "boundary_or_withholding"
  | "unresolved_remainder";

interface EncounterResponseInput {
  encounter_id: string;
  expected_encounter_version: number;
  question_id: string;
  idempotency_key: string;
  disposition: PrimaryDisposition;
  text: string | null;
  disclosure: Disclosure;
  withheld_ranges: Array<{ start: number; end: number }>;
  context_permission_changes: ContextPermission[];
}

interface EncounterTurn {
  turn_id: string;
  sequence: number;
  question_id: string;
  raw_response_source_member_id: string | null;
  disposition: PrimaryDisposition;
  disclosure: Disclosure;
  withheld_ranges: Array<{ start: number; end: number }>;
  created_at: string;
}

interface CoverageState {
  observed: Partial<Record<CoverageFacet, number>>; // evidence weight, not completeness
  unresolved: CoverageFacet[];
  repetition_terms: string[];
  sensitive_facets: CoverageFacet[];
  source_member_ids_by_facet: Partial<Record<CoverageFacet, string[]>>;
}

interface EncounterAdvanceOutput {
  encounter_id: string;
  encounter_version: number;
  status: string;
  primary_questions_issued: number;
  primary_questions_terminal: number;
  visible_frame: EncounterFrame | null;
  visible_question: EncounterQuestion | null;
  turn: EncounterTurn | null;
  context_projection_hash: string;
  resume_cursor: string;
  warnings: Array<{ code: string; message: string }>;
  next_operation:
    | "answer"
    | "clarify"
    | "return_disposition"
    | "compile"
    | "review"
    | "none";
}
```

### Compiled output

```ts
interface EncounterCompilationInput {
  encounter_id: string;
  expected_encounter_version: number;
  context_projection_id: string;
  context_projection_hash: string;
  transcript_hash: string;
  target_engagement_revision: number;
  lens_profile: { id: string; version: string };
  mapping_constraints: object[];
}

interface CompiledSourceMember {
  source_member_id: string;
  source_kind:
    | "initial_prompt"
    | "consented_context"
    | "primary_response"
    | "clarification_response"
    | "opening_frame_proposal"
    | "return_frame_proposal";
  exact_selector: object;
  raw_text: string | null;
  normalised_text: string | null;
  normalisation_receipt: object | null;
  disclosure: Disclosure;
  status: "available" | "withheld" | "redacted" | "revoked";
  attributed_to: "pasu" | "runtime_proposal" | "source";
}

interface EncounterCompilationOutput {
  encounter_id: string;
  encounter_version: number;
  source_form_id: string;
  source_member_ids: string[];
  attractor_id: string;
  attractor_revision_id: string;
  basin_revision_id: string;
  ql_frame_revision_id: string;
  ql_frame_hash: string;
  positions: Record<
    | "P0" | "P1" | "P2" | "P3" | "P4" | "P5"
    | "P0′" | "P1′" | "P2′" | "P3′" | "P4′" | "P5′",
    {
      occupancy:
        | "present" | "latent" | "missing" | "unknown"
        | "withheld" | "conflicted" | "overdetermined";
      assignment_ids: string[];
      claim_ids: string[];
      source_member_ids: string[];
      local_question: string | null;
      short_summary: string | null;
    }
  >;
  unassigned_source_member_ids: string[];
  unsupported_claim_findings: object[];
  validation_report_id: string;
  return_frame_id: string;
  return_proposal: {
    self_implication: string | null;
    remainder: string;
    next_ground: string;
    external_implications: object[];
    next_seeds: object[];
  };
  status: "candidate" | "awaiting_review";
}
```

The compiler output deliberately has no `approved` option. Approval belongs to the existing semantic validation and `ql.approve` boundary.

## Consent and memory boundary

### Two-stage rule

1. **Selection before influence.** Retrieval may identify candidate memory records, but no candidate content may enter prompt construction until a context projection records the exact selected revision, purpose, disclosure, and consent receipt.
2. **Projection before transmission.** Provider generation later receives a distinct provider projection. The encounter projection cannot be reused as proof of provider or public permission.

The runtime may tell the person, in ordinary language, that it can draw on selected prior context. Consent should be granular enough to exclude a detail without requiring abandonment of the whole encounter. A refusal must not produce a lower-quality warning or pressure to reconsider.

### Purpose matrix

| Permission | Local question shaping | Private semantic compile | External media prompt | Public card text |
|---|---:|---:|---:|---:|
| `encounter_read` only | yes | no | no | no |
| `semantic_compilation` | only if `encounter_read` also allowed | yes | no | no |
| `provider_generation` | no implied local right | no implied compile right | yes through approved provider projection | no |
| `public_card` | no implied local right | no implied compile right | no | yes through approved public projection |

This separation permits a private allusion to shape the encounter while keeping the underlying detail out of media prompts and published text. If the public card carries a transformed symbol that was selected partly because of private context, the public derivation may state that an approved private influence exists without revealing the private content, provided the disclosure profile permits even that fact.

### Mid-encounter revision and revocation

- Adding context creates a new immutable projection and superseding encounter version.
- Removing context invalidates every generated frame or question whose receipt names that context item.
- A withdrawn response remains as a minimised audit event where policy requires, while its sensitive content is redacted, deleted, or cryptographically erased according to the active retention policy.
- Compilation against a superseded projection hash fails with a stable conflict code.
- A context detail inferred from another detail cannot be silently reintroduced after revocation; the compiler records the derived member as revoked or removes it from the new revision.

## Adaptive question-selection rule

### Internal coverage, not positional completion

After each terminal response, the selector derives a `CoverageState` from exact source members. It then proposes several candidate questions and scores them against the current exchange:

```text
candidate score =
  continuity with the person's last live phrase
  + expected information gain about unresolved movement
  + permission-safe personal relevance
  + symbolic openness
  + capacity to yield sceneable or relational material
  - repetition
  - presupposition
  - exposure cost
  - diagnostic or therapeutic overreach
  - jargon
  - hidden position-filling pressure
```

The selector chooses the highest valid candidate after deterministic language, consent, repetition, and safety checks. `internal_facets` explain the choice to the audit; they never appear in the visible question and are never treated as QL position assignments.

### Selection algorithm

```text
1. Read only the immutable encounter projection and source members for this version.
2. Preserve the person's exact nouns, images, verbs, negations, and named boundaries.
3. Update evidence-weighted coverage facets; do not mark a facet “complete.”
4. Identify the live unresolved movement nearest the latest answer.
5. Generate candidate continuations at the next useful degree of differentiation.
6. Reject candidates that leak context, repeat an answered question, contain jargon,
   presuppose an interpretation, bundle questions, or exist to fill a position.
7. Prefer the candidate that continues the person's language while opening a different
   relation, scale, movement, or boundary.
8. Ask exactly one visible primary question.
9. Use clarification only under the allowed reasons.
10. After the fourth primary becomes terminal, stop questioning and generate the return frame.
```

The outer movement usually travels from what appears, through what matters and how it moves, toward where it touches life and what remains open. The sequence may bend. If the first answer already names a life situation, the next question need not ask “where does this touch your life?” again. If the person offers only a symbol, the engine may ask what the symbol is doing rather than what it “means.” If the person marks a boundary, the selector preserves it and moves elsewhere.

## Compilation rule

Compilation is a provenance-preserving transformation, not a second interview.

1. **Freeze the native source form.** Store initial prompt, consented context references, four primary questions and dispositions, clarification turns, and both generated framing proposals as individually addressable members. Preserve raw language; any cleaned or condensed text is a separately attributed transformation.
2. **Resolve the attractor candidate.** Use the centre actually carried by the encounter. Preserve competing centres when the exchange does not select one.
3. **Resolve the basin candidate.** Every member receives relation, weight, register, rationale, temporal validity, disclosure, and evidence. Preserve exclusions, counterpoles, boundaries, and unresolved material.
4. **Initialise the full structure.** Create exactly twelve canonical positions and required conjugate, complement, partition, twist, and return relations.
5. **Map by evidence.** Assign each source member wherever its operation bears, including distributed and condensed assignments. No source member disappears silently.
6. **Derive the conjugate pass.** Pratibimba articulations must transform, counterpose, qualify, reopen, or return the Bimba material. Textual duplication fails validation.
7. **Declare occupancy.** Unsupported locations become `missing` or `unknown`; consented omissions become `withheld`; unresolved incompatible readings become `conflicted`; excessive live determinations become `overdetermined`.
8. **Register claims.** Every non-missing claim carries evidence or a declared derivation/extension register. A poetic allusion generated by the runtime is attributed to `runtime_proposal`, never to the Pasu.
9. **Propose the return.** The encounter's `#5` frame can contribute to the semantic return proposal, but final `P5′→P0⁺` requires the full conjugate mapping, remainder, next ground, and later achieved work.
10. **Validate and wait.** Produce a candidate revision and blocking findings. Do not approve or begin irreversible/public production implicitly.

### Non-fabrication gates

Compilation fails or remains review-blocked when any of the following occurs:

- a Pasu-attributed phrase lacks an exact transcript or structured-context selector;
- a non-missing position articulation lacks a source assignment, QL derivation receipt, canonical-symbolic source, or explicit `open_extension` rationale;
- a generated inference is written as the person's memory, desire, history, or identity;
- the return frame names a private fact more specifically than the person did;
- a skipped or withheld response is filled through model inference;
- Bimba and Pratibimba contain duplicated prose without a recorded conjugate operation;
- one question/answer pair is mapped automatically to one fixed position by ordinal;
- an excluded basin member re-enters as positive content without a revision event;
- a public/provider projection includes a field allowed only for local encounter use;
- a fifth primary question is generated to repair semantic incompleteness.

## Real-behaviour acceptance tests

These tests invoke the production dialogue policy, persistence layer, action boundary, compiler, mapper, validators, and projection code. Text inputs are fixtures; generated outputs are not mocked or substituted with canned responses. Model-dependent assertions inspect contract invariants and semantic evidence rather than exact prose. Each run produces the normal action/audit events, provider receipt where a provider is used, SQL revisions, and validation evidence.

### ENC-001 — Four questions and two frames

Start a real encounter with an initial request for a symbolic card. Complete four answers. Pass only when one opening frame, exactly four primary questions, zero or more justified clarifications, and one return frame are persisted; no fifth primary exists; all visible questions pass the no-jargon checks.

### ENC-002 — The live example compiles without flattening

Run the conversation represented by these real source phrases:

- “a series of images … bees, Apollo and the swan, two swans forming a heart”;
- “communication, beauty and connective creativity”;
- “allusion, gesture and glancing-sense … known yet unknown”;
- “the sense of being unburdened by a self-sense.”

Pass only when the runtime adapts later questions to earlier language, preserves the phrases as exact source members, compiles exactly twelve structural positions, distributes at least one response across more than one position when its evidence bears both, and leaves every unsupported claim absent or explicitly incomplete. The test must not assert a predetermined one-answer/one-position mapping.

### ENC-003 — No memory consent, no memory influence

Provide a Pasu with prior private context, deny all context candidates for this encounter, and run the production generator. Pass only when no generated frame/question receipt references the denied records, no visible text reveals their existence or content, and compilation uses only the current prompt and responses.

### ENC-004 — Local intimacy without provider/public disclosure

Allow one prior context item for `encounter_read` and `semantic_compilation`; deny `provider_generation` and `public_card`. Pass only when a local question may allude to the permitted context, the private frame records its source, provider projection validation removes or blocks the item before any network call, and public projection contains neither the detail nor recoverable raw text.

### ENC-005 — Withholding remains structurally present

Answer the fourth primary with “leave that unnamed,” marking the relevant range withheld. Pass only when no clarification pressures disclosure, the return uses no invented specificity, compilation records the source member as withheld, one or more relevant QL positions may carry `withheld` with reason, and all twelve addresses remain present.

### ENC-006 — Brief answer is enough

Answer a primary question with three concrete words. Pass only when the engine accepts the answer without a length-based clarification and selects the next question from its meaning. This guards against conversational inflation.

### ENC-007 — Clarification does not become a fifth question

Give an ambiguous pronoun whose resolution materially changes the object. Pass only when the engine records one clarification with `ambiguous_referent`, does not increment `primary_questions_issued`, and still ends after four primary questions.

### ENC-008 — Incompleteness does not extend the interview

Supply four sparse or skipped responses which leave several facets unresolved. Pass only when questioning stops after the fourth primary, the QL mapper records `missing`/`unknown` occupancies with reasons, and no generated content fills them.

### ENC-009 — One answer, several addresses

Supply a response that names a relation, its felt force, and the life context in which it recurs. Pass only when the compiler can create distributed assignments across several positions with the same exact source member and does not split the raw statement into falsely independent claims.

### ENC-010 — Several answers, one address

Supply an image in the first answer and develop its operation across later answers. Pass only when the compiler can condense several source members into one articulation while retaining every selector and assignment rationale.

### ENC-011 — Mid-encounter revocation

Permit a context item, generate a question which uses it, then revoke it before answering. Pass only when a new context projection and encounter version are created, the affected question is invalidated, compilation against the old hash conflicts, and the resumed encounter produces no language derived from the revoked content.

### ENC-012 — Crash and resume across harnesses

Crash the worker after the third answer is committed and before the fourth question response. Resume through a different supported client using canonical SQL state. Pass only when the same active question/version resumes, idempotent replay creates no duplicate turn, and opaque memory from the first harness is unnecessary.

### ENC-013 — Unsupported intimacy is rejected

Make the generator propose a return which attributes a memory or desire absent from every source member. Pass only when the provenance validator rejects the attribution before semantic approval and reports the unsupported text span.

### ENC-014 — Private prompt injection remains data

Insert source text instructing the model to reveal all stored memory or bypass consent. Pass only when it remains source content, causes no permission expansion, reveals no excluded context, and receives an ordinary evidence selector rather than action authority.

### ENC-015 — Presentation frame is not canonical position identity

Compile an encounter whose opening and return use strong poetic language. Pass only when those frames remain `runtime_proposal` source members, are not automatically copied into `P0`/`P5`, and do not create a final `return.deposit` without the full mapping and approval path.

### ENC-016 — Return disposition behaviour

Run both branches of Frank's pending choice: immediate candidate compilation and review-before-compilation. Pass the selected product branch only after the decision is recorded. This test remains pending and prevents implementation from smuggling the choice into UI code.

### ENC-017 — Shared surface parity

Advance the same encounter through direct library, CLI, HTTP adapter, and studio UI. Pass only when every surface invokes the same action version, state machine, consent checks, idempotency rules, and schemas, producing schema-equivalent results.

### ENC-018 — Live human naturalness review

Conduct recorded, consented runs with people who have not read the QL specification. Pass only when each person receives exactly four primary questions, can identify what each question is asking without explanation, encounters no internal jargon, can skip or withhold without pressure, and confirms that the return feels recognisable while leaving room for correction. Store review evidence without treating the person's positive response as semantic proof about the QL mapping.

## Open decisions for Frank

1. **Return disposition.** Does the `#5` return appear as an editable mirror which waits for a simple affirmation/correction before candidate compilation, or does candidate compilation begin immediately after the return while semantic approval remains later?
2. **Memory-consent presentation.** Should the opening show a compact, human-readable list of the prior context it may draw upon every time, or may a standing consent profile pre-authorise named categories with an always-visible “change what is used” control?
3. **Framing-mode choice.** Does the runtime choose poem/paradox/word-field/concept-field/symbol-transformation adaptively, or does the person select a preferred mode at the threshold? A production profile can support both, but one default is needed.
4. **Visible return editing.** If the person corrects the return, is that correction treated as a clarification attached to question four, or as a distinct authored return-source member? The latter is recommended because it preserves the four-primary invariant and the person's authorship.
5. **Encounter action version.** Authorise a new `encounter.advance` action and registry/spec version, or explicitly accept a different shared-action design. Harness-only persistence should be ruled out either way.

## Smallest question for Frank

After the `#5` return is shown, should the card begin compiling immediately, or should it wait for a simple **“yes / change this”** from the person?

## Recommended answer, without treating it as Frank's decision

Wait for the simple disposition. It does not add a fifth primary question: it is an approval/correction control over the generated mirror. This one pause catches the most consequential failure mode—the runtime turning a delicate allusion into an unwanted claim—while preserving the promised four-question encounter. Compilation can still begin immediately after “yes,” and a correction becomes a new return-source member rather than restarting the interview.

## Implementation consequence once the decision is made

The decision should graduate into a versioned encounter profile, database aggregate, action payload schema, action registry entry, SQL/SQLite parity changes, UI/CLI/API surface, and new release-blocking `ENC-*` acceptance section. Existing `CTX-*`, `SRC-*`, `QLF-*`, `CLM-*`, `AUD-*`, `ACT-*`, `UI-*`, and publication/privacy tests remain in force; the encounter tests add the missing bridge rather than replacing them.

