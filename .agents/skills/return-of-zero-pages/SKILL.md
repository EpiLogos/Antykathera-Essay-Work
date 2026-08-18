---
name: return-of-zero-pages
description: Use when developing a single field-page record for The Return of Zero across symbolon, matheme, mytheme, or episteme.
---

# Develop a Return of Zero Field Page

A field page is the developed account of one element, standing alone and implicating the rest. It surfaces a canonical body — source house, argument node, theorem spine, concept, image, history, dossier, path, or other ratified record — in the register's own form.

## When to use

- Building a page from a ratified quilt/census element before prose exists.
- Developing a page from a live canonical node as the rooms fill.
- Converting a working-shelf item into its publication-body home.

Do not use for essay drafting inside `THE-RETURN-OF-ZERO.md`; use `return-of-zero-write` for that.

## Governing page-form law

The sixfold is a **raw QL relational chassis, not a universal semantic template**.

The canonical blank body is:

```markdown
# <record title>

## #0

## #1

## #2

## #3

## #4

## #5→0
```

Do **not** pre-fill these positions with universal headings such as `In-quantum`, `Definition`, `Operation`, `Pattern/Identity`, `Context`, or `Quintessence`. Those may be valid readings for a particular page, but they are not the semantics of the positions themselves.

The foundational QL qualities constrain interpretation without fixing page semantics in advance. In the native process account, the positions can be tested as ground/inherited field; first determination; differentiation/selection; relation/pattern/decision; contextual recomposition; and recognition/return. These are orientation pressures, not mandatory labels or a prose recipe. A Matheme, Mytheme, Episteme, root Symbolon, source-facing dossier, or transverse path can realise the sixfold differently while remaining answerable to the same relational qualities.

At page-creation time, derive what each position actually means for this record from:

1. the record's positive proposition or governing image/operation;
2. its register contract and `record_type`;
3. its inherited relations and outgoing return obligations;
4. the native QL foundational qualities;
5. the ratified quilt/census decision that gave the record its office.

Only then may a section receive a descriptive subtitle, for example `## #2 — <page-specific meaning>`. If a page-specific title would overstate or prematurely freeze the relation, keep the raw `## #N` heading.

## Steps

Each step ends on a checkable completion criterion.

1. **Recover the register contract.** Read the register README for the element's register:
   - `symbolon/README.md` for root relations.
   - `matheme/README.md` for exact operations.
   - `mytheme/README.md` for lived images.
   - `episteme/README.md` for instituted knowledge.
   *Done when you can state the record form the register demands without importing a generic six-heading glossary.*

2. **Resolve the canonical home and ratified office.** Use `tools/source_resolver.py` or `tools/okf-workspace.py find` to locate the element's one home. Read existing frontmatter and any `NOTES.md` (read-only), plus the ratified census/decision that created, retained, merged, split, or rehomed the record. *Done when you have the record's stable identity, declared register, publication office, and exact reason it exists as its own page.*

3. **Open the raw QL skeleton.** Start with exactly the six positions `#0`, `#1`, `#2`, `#3`, `#4`, `#5→0`. Do not assign generic semantic names yet. *Done when the blank page has the six positions and no inherited semantic boilerplate.*

4. **Derive this page's sixfold.** Work from the actual material. For each position ask what distinct relation is being performed here, how it inherits the prior position, and what it makes possible next. Check the result against the foundational QL qualities, but do not force every record to paraphrase the same process vocabulary. *Done when each position has a page-specific function that can be justified from the record itself.*

5. **Title only what has been earned.** Add page-specific subtitles where they increase precision. Keep raw numeric headings where a label would reduce a polyvalent relation to one gloss. *Done when no section title could be copied unchanged into an unrelated page merely because both pages are sixfold.*

6. **Draft the page body.** Develop the element at full register rather than as a diluted summary. The page must make its admission relations and return routes legible, but those relations need not be forced into predetermined positions if the record's own sixfold places them differently. *Done when the page stands alone, implicates the wider field, and every relation is carried in the prose or declared links.*

7. **Attach status and source relation.** Every claim carries `claim_status` (Derived / Argued / Offered / Open). Every external source relation is named precisely (Extracted / Paraphrased / Argued from / Resonant with, or the repository's ratified equivalent). *Done when frontmatter and body declare both without weakening authorial claims because evidence work remains open.*

8. **Check non-duplication and return.** The page surfaces the canonical body; it does not copy another record merely to appear complete. If another canonical record carries the primary derivation/evidence/image, link it and state this page's distinct operation. Confirm the page has an outgoing route back into the argument, section, path, or whole. *Done when removing the page would lose a unique operation, while removing duplicated prose would not erase primary evidence.*

## Common mistakes

- Treating the six QL positions as a global content taxonomy.
- Hard-coding `Definition / Operation / Pattern / Context / Quintessence` before reading the record.
- Using the foundational QL qualities as compulsory prose headings instead of relational constraints.
- Treating `#0` or `#5→0` as decorative framing rather than real positions in the record's own sixfold.
- Letting a mytheme page prove a matheme claim, or an episteme page present itself as derivation.
- Duplicating a source house's passage cards instead of surfacing their account.
- Creating a page because a term occurs often rather than because the ratified census found distinct aletheia-work.
