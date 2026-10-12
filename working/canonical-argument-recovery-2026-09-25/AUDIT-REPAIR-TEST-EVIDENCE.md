# Recovery audit repair — executed evidence

The test run concerns the recovery detector, not semantic acceptance of the essay.

## Reproduction

Retrieved `tools/audit-canonical-argument-recovery.py` and its test module from GitHub. Before execution, their local bytes were checked against Git blob hashes:

- audit: `205b114caceb01cd522c63a9551dcecf8e726c4e`
- tests: `e0e087239204ff097c3de1deb3ab5fdb92595d27`

Both matched. Running the existing three tests produced one failure: `test_ai_consciousness_guard_is_hard_failure`. The detector missed `The technical architecture does not establish phenomenal subjectivity.` because its first pattern required the technical subject after the negation, while the second only caught unresolved-status constructions.

## Repair and rerun

Command executed in the validation workspace:

```sh
python -m unittest discover -s tests -p test_canonical_argument_recovery_audit.py -v
python -m py_compile tools/audit-canonical-argument-recovery.py
```

Result: **17 tests passed**; compilation passed. Coverage includes the original failing sentence, its wrapped form, the actual legacy C35 sentence, all canonical sixfold types and ID-only records, duplicate/reordered positions, empty section shells, visible link labels rather than link destinations, source-line offsets, blockquotation review, fenced examples, protected sources, missing corpus and empty selection, and public etymology histories remaining in scope.

Tested resulting bytes:

| File | Git blob SHA | SHA-256 |
| --- | --- | --- |
| `tools/audit-canonical-argument-recovery.py` | `63b838f979582bcb4399665a07e3e9122b288c67` | `877610a50763e4105f8c4ae929464f7b3b5f97b5ecb5903d7faa6bd1050837d6` |
| `tests/test_canonical_argument_recovery_audit.py` | `2fc2293f56c74e21de06ab3c014f499db9301711` | `07b5f13af1b8c20eb66b833e26a05fdeeccd103bc7b5ba375145143275a6aa6c` |

## Scope

These are executed detector regressions in a source-hash-verified partial validation workspace. The entire repository was not available to this runtime; the full repository test suite, generated projections and whole-field semantic review are not certified by this run. Pattern findings identify passages for review and do not establish philosophical faults by themselves. No automatic prose rewrite is performed.
