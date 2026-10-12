# Local validation — preliminary failure and correction

These are local results, not a GitHub publication receipt. Both runs used `python3 -m unittest discover -s tests -v` on the full native checkout. The 4,105 tracked regular files were hashed before and after each run; neither run mutated them. No test or discovery rule was modified.

## Preliminary run

132 tests; four failures; one unavailable-AIKit skip. Process elapsed 229.034 seconds; unittest reported 227.386 seconds.

The expected quality-coverage failure remained. Three additional failures were caused by raw Markdown preimages under the working evidence directory being discovered as live typed records:

- `test_source_houses_and_reading_routes_are_traceable_in_bounded_context`: source-house counts `188 != 187`.
- `test_status_discovers_the_real_typed_workspace`: argument counts `76 != 72`.
- `test_doctor_clears_canonical_source_and_room_integrity_debts`: returned `{'duplicate-source-house': 2, 'missing-register': 48, 'thin-section': 1, 'unresolved-link': 2}` rather than satisfying its forbidden-debt assertion.

All eight preimages were stored losslessly as deterministic gzip. Their decompressed bytes were checked against the original Git blobs. Builders were rerun. The evidence remains recoverable without presenting copies as current canonical records.

## Complete rerun after storage correction

132 tests; 130 passed; one quality-coverage failure; one unavailable-AIKit skip. Process elapsed 268.2 seconds. All 4,105 tracked regular files remained unchanged.

The remaining failure is `test_canonical_graph_has_no_missing_quality_surfaces_or_governing_dangles`. Its concept source-anchor findings are C25, C26, C28, C33, C36, C37, C38, C39, C42, C43, C45, C46, C48, C49, C50, C52 and C64. Its movement findings are M16, M25, M32, M36 and M47; M25 names both warrant and counterpressure surfaces, the others counterpressure surfaces. Those movement bodies are deferred by the author's instruction. The foundational concept findings remain open and are not waived.

## Exact final-candidate distinction

A subsequent `git diff --check` found one extra EOF blank line in the Hatcher source. That blank line was removed, its exact postimage and payload/source hashes updated, and source/navigation projections rebuilt. The prior complete local-suite result is therefore not represented as a byte-identical validation of the final candidate. The native integration workflow must run the unchanged full suite against the exact final payload and preserve its actual output before publication.

The six public recovery records passed the unchanged strict detector with zero hard errors and 39 review candidates, individually reviewed. The 17 detector regression tests and the 113 scoped link checks passed. The central-plan change and Hatcher source have their separate scope. Room-depth and pre-manuscript structural checks are not a 48-movement semantic review.
