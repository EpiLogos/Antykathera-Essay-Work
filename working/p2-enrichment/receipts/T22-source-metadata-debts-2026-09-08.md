# T22 scoped source metadata diagnosis — 2026-09-08

Current doctor confirms 11 missing-passage-locator and 51 missing-passage-provenance debts: 62 debt pairs on 51 cards in 15 houses. Every pair exists in the pre-integration T22-Pauli-Jung-source-integration-hygiene.json baseline. This is a dated workspace baseline comparison, not a claim that every card was already committed in HEAD.

No affected card belongs to the owned Pauli SOURCE; its parsed cards retain locators and provenance. The owned von Franz house has no admitted passage cards. Therefore no canonical SOURCE correction is required or made within this ownership scope. LSJ q009 and LewisShort q006 came from E6 proposals but were integrated in parent-owned houses; their formatting corrections remain proposals for the parent.

## Exact causes and proposed repairs

- 34 external cards contain inline fields. Verification following Locator on the same line is invisible to the line-start parser. Three Laozi cards additionally place Locator after Paraphrase. Reflow existing field labels onto separate lines; all non-whitespace content survives exactly.
- Eight external cards use the unsupported combined label `Locator and verification`: ATILF q001, LewisShort q001–q006, LSJ q009. Extract the already stated headword/scope as Locator and retain the entire original combined payload as Verification, including read date, carrier and all limitations.
- Nine Taylor cards ct08–ct16 need explicit per-card Provenance. ct08–ct15 point to the actual native core text. ct16 points to its distinct authorial companion at line 47 and retains its pending authorial decision. It is not promoted to core theorem or external Descartes evidence. These insertions do not change curator wording or source standing.

The exact machine packet is `working/p2-enrichment/page-packets/T22-source-metadata-debt-proposals.json`: one entry per card, canonical path, stable passage ID, missing fields, original/current hashes, exact old/new metadata text, and parsed result. All 15 source snapshots still matched current bytes at validation. Owners must rerun effects and compare fresh bytes before applying; parent may concurrently repair curator content.

## Verification and boundaries

All 51 proposed card texts pass the repository's actual `Workspace._field_from_card` locator/provenance parser in memory. This verifies the proposed field recognition, not an applied doctor-zero state. The current real doctor and full source snapshots are retained in `working/p2-enrichment/page-packets/T22-source-metadata-debts-private.json`. No evidence was invented and no source/claim/quotation status was upgraded.

No canonical files, NOTES, shared coverage, projections or index were written. Index was empty at final inspection; no staging command was issued. Parent retains curator and room-projection repairs. The six-test suite was not rerun for this private diagnosis, and its two reported failures are not claimed resolved. Conjugate navigation remains accepted and unstaged, awaiting its separate index grant.
