# Field prose pass — shared brief (read in full before touching any file)

Project root: `/Users/admin/Central/Work/O-I/Antykathera-Essay-Work` (branch `essay/field-prose-pass-20261006`). Content root: `submission-package/essay/`. You are one of five area owners; you never spawn subagents of your own.

## Why this pass exists

The field files have the right content and bones, but the prose breaks almost everything the writing protocol exists to fix. The worst case so far, the Hephaestus / Ares and Aphrodite page, writes in the wrong style everywhere except its quotations:

- it buries the argument in fake-poetic styling;
- or it never states the argument properly;
- or it states it too early, before the context that earns it;
- and it runs constant strings of "the X … the Y …".

This pass is exhaustive and must genuinely enrich. It is not cosmetic: every page should end up stating its argument clearly, in the right order, with its referents developed. A page's reader should be able to remove every link and record ID and still follow an intelligible argument: premise → operation → consequence.

## Read first (in this order, every time you begin or resume; reread PROSE-STANDARD before each new file group)

1. `AGENTS.md`, then `return-of-zero-orienting-principles.md`, then `the-return-of-zero-central-plan.md` (skim the plan to the sections your files serve; do not read it linearly if you have the orienting principles).
2. `PROSE-STANDARD.md`, in full, including "Lessons carried from M04", "M05", "M06" and "M01–M03". This is the governing standard.
3. `.agents/skills/return-of-zero-write/SKILL.md` and `.agents/skills/return-of-zero-links/SKILL.md`.
4. `working/s01-hardening-2026-10-01/SECTION-UPDATE-LEDGER.md` for canon rulings. Apply the rulings that bear on the prose you are editing (e.g. I-Consciousness is the whole; Objective Internality is Life / Mind; Māyā's contextual place). Do not execute the ledger's structural items (renames, new houses, room rebuilds); if a page needs one, log it for Frank.
5. The model of the target voice: `submission-package/essay/CONFRONTING-THE-LIMIT-S01.md`. Read at least M01 (line ~36) and M04 (line ~339) before editing anything. Notice what it does: the case is told plainly first; the operation is derived inside the case; sentences have real subjects and verbs; long sentences hold several dependencies with *because / by / thus / insofar as*; first-person plural does the work; there are no riddles.

## The faults to fix (judge by reading each passage in its page, never by pattern-matching)

- **Withheld affirmation.** State what the argument has earned. Do not hedge it into a safer neighbour or manufacture counterpressure against it. A boundary is admitted only if it names its carrier (a source, a proof hypothesis, an implementation state, a canonically live tension).
- **The argument missing, buried or premature.** Each page must say plainly what it claims and why. Build the context (the case, the operation, the source) before the claim lands. The because must be on the page: premise → operation → consequence.
- **Fake-poetic lines.** Riddles, aphoristic flourishes, "X makes a minimal journey", "alive in the distinction", "the cycle completes", "gives X its Y". Replace each with what is actually happening, stated as an operation.
- **Strings of "the".** "The X, the Y, the Z of the W." Rebuild with real subjects and verbs.
- **Nouning.** Abstractions acting as agents ("power enters through…", "the diabolical operation makes…", "the gathering arrests reciprocity", "the account protects itself"). Say who or what does what ("the question of power becomes pressing"; "dia-ballein in its diabolical sense makes…"). Opening-rate check: if more than about one sentence in ten opens "The …", rebuild openings by leading with an actor, the case, or the relation. Counts check a rebuild, they never drive one.
- **Construction tics.** "x was there before y"; "x is y, without a and b"; announcing sentences ("Here is why…", "Jung gave the reason."); one-line paragraphs; list-like prose. Merge short paragraphs into flowing ones; split any six-clause sentence. For every sentence under about ten words ask: does it state something or announce something?
- **Register.** One mode per scene, narrated or addressed, never a muddle. No "you" casting the reader in a role; use "we" or the third person. Tenses track the scene. No deictic "this evening" inside a generic present.
- **Mythemes.** A myth compresses a psychodynamic into persons and deeds. Tell the story clearly and in full, then unfold it into the operation it carries. Do not decorate the operation with mythic adjectives. R6: a mytheme discloses through the action of the whole image, which is a different office from formal proof or historical attribution. Say which office is operating.
- **Defensive disclaimer clusters** ("neither… nor…", "this does not establish…", "remains distinct from…", "retains its own office…") stacked after a claim: a page may need one exact boundary, stated after the positive claim and naming its carrier. Ten stacked disclaimers are the fault, not the cure. Lead with the claim; state the one boundary that is real; cut the rest.

## Enrich, don't just subtract

- Where a page names a concept, source or relation without developing it, develop it from the corpus: the linked argument and concept records (`section-rooms/arguments/`, `.../concepts/`), the source houses (resolve with `python3 tools/source_resolver.py <source_id>`), the theorem spine `working/sources-texts-references/10-7-2026-core-theorems-pithy.md`, and the earlier manuscript as quarry (`submission-package/essay/THE-RETURN-OF-ZERO.md`, read-only; `CONFRONTING-THE-LIMIT-S01.md`, read-only).
- Give each claim its concrete case. Define a term by its own carriers before saying what follows from it. Introduce others' ideas as concepts with their operation ("Heidegger's concept of *Bestand*, standing-reserve, names…").
- Never invent quotations, pages, dates or facts. If you add a fact, you have read it in a corpus file in this session; if you cannot find it, do not add it, and log the gap for Frank.
- Never pad. A page may get shorter or longer; length is judged by whether the argument is carried.

## Canon (binding)

- Write **syn-ballein**, never "sym-ballein", in prose you write or touch. Leave link text that is a generated title, filenames, record IDs and `Sym-Ballein` node titles as they are.
- Healthy polarity is written `(−1)/(+1)` (U+2212 minus; negative pole first). Appropriation always appears in **both** chiralities: `(+1)−(−1)=+2` and `(−1)−(+1)=−2`; `±2` is hardened opposition against clean oscillation; name the mirror in a case (the public's `+2` is the scapegoat's `−2`). Cancellation is `(−1)+(+1)=0`. Syn-ballein is `(0/1)/(1/0)`.
- I-Consciousness is the whole; Objective Internality is Life / Mind ("a mind is lived, a life is minded"). Subject and God are two signs of one referent.
- Never the term "conspiracy theory". Describe the structure instead.
- `X/x` is authorial QL notation; never attribute it to Jung.
- Internal-corpus chats (`taylor-2026-*` chat houses, `chat-logs-for-quilting`) are provenance, never citations.
- Notation mechanics per `PROSE-STANDARD.md` §Mechanics: mathemes in backticks with Unicode; display maths in `$$…$$`; QL positions keep `#` (**#4**).

## Do not touch

- Any `*-NOTES.md`; `AUTHORIAL-TEXT.md`, `READING-*.md`, `SCRATCH.md`, `HISTORY-*.md` (protected).
- Generated files: `ROOM-*.md`, `maps/navigation/`, `SOURCE-INDEX.md`, `MAIN-SOURCES.md`, `PASSAGE-LEDGER.md`. If a file's frontmatter or header says it is generated, skip it and log it.
- Source houses under `symbolon/episteme/sources/` (out of scope, read-only for you).
- `THE-RETURN-OF-ZERO.md`, `CONFRONTING-THE-LIMIT-S01.*`, anything under `working/` except your own log in `working/field-prose-pass/`.
- `symbolon/mytheme/poetry/` (Frank's verbatim poems; `test-site/src/poems.js` is canonical and immutable) and `symbolon/matheme/definition/harmonics-and-recount.md` (Frank's parallel branch touches it).
- Frontmatter: do not change it. Record IDs, heading anchors (`<a id=…>`, `^block-ids`), and every link and its target stay. You may reword a link's visible text only where its sentence is rebuilt, and you keep every link target. If you must move a link into another sentence, it still lands where the same relation is argued.

## Preserve

- **Frank's own sentences, wherever they stand.** They are recognisable by first-person commitment, puns that argue, the actual case, derivation inside the material, registers crossed in one move, long sentences with *because/by/thus*. Rebuild what lets them down (the opener, the sandwiched middle, the recap closer); do not replace them. When in doubt whether a sentence is his, keep the wording and log the doubt.
- **Verified quotations exactly**, including their citations, locators and the notes around them. Block quotes and passage cards are not yours to reword.
- **Required record structure**: register declarations that open depth records, warrant / counterpressure surfaces (sections such as "Source and authored scope", "Counterpressure", "Warrant", "Tension"), "route of return" sections, status marks (Derived / Argued / Offered). Keep the sections and headings; rewrite their prose in positive form.
- **Link relations.** `tools/build-navigation.py` reads the relation word in the sentence around each link (one of: `derives`, `grounds`, `defines`, `historicises`, `sources`, `qualifies`, `tests`, `figures`, `embodies`, `extends`, `compares`, `presages`, `returns-to`; a bold word anywhere in the sentence, or a plain word beside the link). When you rebuild a sentence that carries a link, keep a true relation word beside it, and make the sentence actually enact that relation (never insert the word as decoration). A link whose sentence names no relation is reported as `unnamed`; do not create new `unnamed` links.
- Argument/concept record IDs such as A13, C23 are addresses. The prose must carry the reasoning without them.

## How to work, file by file

1. Resume check: if `working/field-prose-pass/<area>-LOG.md` exists, read it and continue from the first file without a "DONE" entry.
2. For each file: read it whole; read the records it links to when they bear on a claim; recover the page's actual claim; mark Frank's sentences; mark the quotations; then rebuild. Write the file as soon as it is finished (Edit/Write in place). Reread the result as one piece. Run the verification pass from PROSE-STANDARD ("How a passage is repaired", step 8): list every sentence under ten words and ask whether it states or announces; count the "The …" opening rate; search for each fault's tells and reread every hit in place; make sure every link target and anchor survives (`git diff` the file and check that the set of `](…)` targets and `<a id` anchors is unchanged except for intended edits).
3. Append to your log immediately after each file (log format below). Do not batch log entries.
4. Do not run git commit; the coordinator commits per area. You may use `git diff`/`git status` read-only.
5. Files that are pure index lists, tables, or data (a README that is only a directory listing) need only an honest light pass; say so in the log rather than inventing prose. Files that are already in the right voice are left alone with a log line saying why.

## Log format (`working/field-prose-pass/<AREA>-LOG.md`, append-only)

```
### <path relative to submission-package/essay/>  — DONE | SKIPPED | LEFT-FOR-FRANK
words: <before> → <after>
changed: <2–5 lines: what was wrong, what you did; name the worst patterns>
enriched from: <files you drew on>
for Frank: <passages that need his authorial decision, quoted briefly, or "none">
```

Put anything needing Frank's decision (a sentence that may be his and that fails; a claim the corpus does not support; a canon conflict; a needed structural change) in `for Frank`. Keep these few: decide yourself whenever the standard decides.

## Report back

Return a short report: files DONE / SKIPPED / LEFT-FOR-FRANK counts, total words before/after, the three worst patterns you found, the `for Frank` items, and the one before/after excerpt you are proudest of and the one you are least sure of.

## Corrections from Frank after calibration (2026-10-06) — binding

1. **Length is fine.** Pages will grow; that is wanted. But every page must also shed waffle and redundancy: restating a point already made, stacked disclaimers, padding between claims. Adding nuance is the prime means of doing this: where a sentence repeats, give the facet its own nuance (what only this case adds) instead of the general point again.
2. **Amplification is the method, and inference is welcome when it is grounded in the layers.** Frank's system reads one relation through three layers used *laminarly*: the **mathemic** layer (the notation and its operations: `(−1)/(+1)`, cancellation, appropriation in both chiralities, `(0/1)/(1/0)`, `/ = −/−`, the six and the eight), the **mythemic** layer (the whole image and the action of its persons), and the **epistemic** layer (the systematised records: arguments, concepts, etymologies, histories, sources). Each layer amplifies the others, in the Jungian sense of amplification: a figure is enriched by laying parallels from the other layers beside it until its operation shows. So where a page reads a myth through the operations (Hermes' answer as cancellation, the spectators' `+2` as the lovers' `−2`, Poseidon's surety as the opening the apparatus lacks), that is the method working, not an overreach. Frame it as amplification: say which layers are laid together and what each contributes (for example, "read through the signed arithmetic, the gods' laughter is appropriation charged from the public's pole"), mark the status (Argued / Offered) where the page carries one, and keep each source's own office (the myth discloses through its whole action; it is not a formal proof or a historical attribution). Do not attribute the essay's inference to Homer, Heidegger, Jung or any source. Do not invent: an amplification must lean on something in the corpus (a matheme page, a record, a quilt page, the theorem spine, the manuscript), which you cite in your log. Ungrounded inferences go in the log under `for Frank`, not into the page.
3. **Frank's own sentences.** If a sentence looks like his and the agent suspects it is (e.g. "Comparability precedes opposition"), keep his wording and rebuild around it; search `THE-RETURN-OF-ZERO.md`, `CONFRONTING-THE-LIMIT-S01.md`, the theorem spine and the quilt pages for the sentence before changing it.
4. **Cases carried from the manuscript** (e.g. the sacrificed representative of M03) may be carried into a field page when the manuscript is the source; say so in the log. Scholarly paraphrase from provisional passage cards is acceptable; quote only verified cards.
5. Calibration files already done: `A13-Two-Logics-of-Two-Dia-Syn.md` and `symbolon/mytheme/worlds/hellenic/ares-aphrodite-hephaestus-poseidon/WHOLE.md`. Read them as the calibrated standard for how a rebuilt page looks (tell the case first, derive the operation in situ, link sentences that enact their relation, positive boundary once).
