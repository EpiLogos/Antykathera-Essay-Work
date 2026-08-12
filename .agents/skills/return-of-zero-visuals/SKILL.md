---
name: return-of-zero-visuals
description: Use when generating a plate, diagram, or figure asset for The Return of Zero and landing it in the correct visual domain.
---

# Generate Return of Zero Visuals

Visuals are records plus assets. The record governs; the asset renders it. Each visual type has one home, one contract, and one register voice.

## When to use

- A field page needs a diagram, plate, or figure.
- A cheaper-model subagent is producing the asset in the same pass as its governing page.
- Auditing whether a visual belongs in matheme, mytheme, or episteme.

Do not use to decorate a page without a governing record; visuals are arguments, not illustrations.

## Steps

1. **Classify the visual by operation.**

   | Type | Operation | Home |
   |---|---|---|
   | Diagram | Formal derivation or construction. | `matheme/diagrams/` |
   | Plate | Composed imaginal argument. | `mytheme/plates/` |
   | Figure | Evidential visualisation. | `episteme/figures/` |

   *Done when the visual has a single correct home.*

2. **Read the domain contract.** Open the README in the target domain for the required record fields: proposition, inputs, transformations, invariant, proof boundary, essay blocks, caption, alt text, source dependencies, rights. *Done when you know what the record must declare.*

3. **Follow the LaTeX law.** From `submission-package/essay/quilt/ql-expression-grammar.md`:
   - Display math `$…$` for operated or derived relations.
   - Backticked tokens for naming.
   - Inline `\(…\)` retired.
   - Use the three canonical table shapes and the concentric-mandala layout for QL units.
   *Done when notation matches the expression grammar.*

4. **Produce record and asset together.** The Markdown record and its editable/rendered asset stay in the same domain directory. The record names the asset, the asset does not float without the record. *Done when both files exist and the record links the asset.*

5. **State the inference boundary.** A diagram may simplify presentation but may not omit a step the claimed conclusion requires. A plate's caption must carry the operation the image performs. A figure's construction method and omissions must be declared. *Done when the visual's warrant is inspectable.*

## Domain routes

- Formal derivations: `matheme/diagrams/`
- Composed imaginal arguments: `mytheme/plates/`
- Evidential visualisations: `episteme/figures/`

Never place a visual in the wrong domain because the tooling is handier there.

## Common mistakes

- Treating a plate as a diagram or a figure as a plate.
- Omitting the record and shipping only the image.
- Using inline `\(…\)` instead of display math `$…$`.
- Letting visual arrangement imply a relation absent from declared evidence.
