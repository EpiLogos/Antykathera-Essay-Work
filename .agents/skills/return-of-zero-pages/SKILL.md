---
name: return-of-zero-pages
description: Use when developing a single field-page record for The Return of Zero across symbolon, matheme, mytheme, or episteme.
---

# Develop a Return of Zero Field Page

A field page is the developed account of one element, standing alone and implicating the rest. It surfaces a canonical body — source house, argument node, theorem spine, concept — in the register's own form.

## When to use

- Building a page from a quilt contribution before prose exists.
- Developing a page from a live canonical node as the rooms fill.
- Converting a working-shelf item into its publication-body home.

Do not use for essay drafting inside `THE-RETURN-OF-ZERO.md`; use `return-of-zero-write` for that.

## Steps

Each step ends on a checkable completion criterion.

1. **Recover the register contract.** Read the register README for the element's register:
   - `symbolon/README.md` for root relations.
   - `matheme/README.md` for exact operations.
   - `mytheme/README.md` for lived images.
   - `episteme/README.md` for instituted knowledge.
   *Done when you can state the record form the register demands.*

2. **Resolve the canonical home.** Use `tools/source_resolver.py` or `tools/okf-workspace.py find` to locate the element's one home. Read existing frontmatter and any `NOTES.md` (read-only). *Done when you have the record's stable identity and declared register.*

3. **Open the QL skeleton.** The sixfold is the page's spine:

   | Position | Function |
   |---|---|
   | #0 — In-quantum | The `0/1` incoming: admitted rooms, arguments, presuppositions. |
   | #1 — Definition | First emergence of explicit form from the in-quantum ground. |
   | #2 — Operation | How the object moves, transforms, produces effects. |
   | #3 — Pattern/Identity | Kind, type, formal architecture — who/which/whereby. |
   | #4 — Context | Where/when/whither — horizon and aperture. |
   | #5 — Quintessence | The `5→0` outgoing: analogia, return route to the whole. |

   *Done when the six positions are named for this element.*

4. **Refract the titles through the register.** Derive the semantic titles from the skeleton, the register's record form, and the element's actual material. Do not import a remembered gloss. *Done when each of the six positions has a title specific to this record type.*

5. **Draft the page body.** Write each section:
   - #0 declares `consumed_by_sections` and `consumed_by_arguments` explicitly.
   - #1–#4 develop the element at full register, not in a diluted summary.
   - #5 names the return route into Symbolon and the essay.
   *Done when the page stands alone and every relation is carried in the prose.*

6. **Attach status and source relation.** Every claim carries `claim_status` (Derived / Argued / Offered / Open). Every source relation is named (Extracted / Paraphrased / Argued from / Resonant with). *Done when frontmatter and body declare both.*

7. **Check non-duplication.** The page surfaces the canonical body; it does not copy it. If the same sentence lives in a source house or argument node, replace it with a pointer and prose framing. *Done when removing the page would not erase any primary evidence.*

## Common mistakes

- Pre-deciding titles from a generic template instead of refracting through the register contract.
- Treating `#0` and `#5` as optional framing rather than admission-and-return mechanisms.
- Letting a mytheme page prove a matheme claim, or an episteme page present itself as derivation.
- Duplicating a source house's passage cards instead of surfacing their account.
