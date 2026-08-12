# Video Essay Resource Coverage Report

Generated after the full section download pass on 2026-07-07.

## Coverage

| Section | Images | Metadata records | Download errors |
|---|---:|---:|---:|
| title-matheme-overture | 10 | 10 | 0 |
| edge-of-the-rational | 5 | 5 | 0 |
| images-that-constellate | 7 | 10 | 3 |
| fall-and-what-it-reveals | 6 | 6 | 0 |
| two-deaths-one-minus-sign | 10 | 10 | 0 |
| the-definition | 8 | 8 | 0 |
| quaternal-logic | 9 | 9 | 0 |
| winds-round-one-torus | 15 | 19 | 4 |
| the-return | 9 | 9 | 0 |
| the-edge | 11 | 11 | 0 |
| maya-and-the-code | 8 | 8 | 0 |
| epi-logos | 10 | 11 | 1 |

Total actual image files: **108**.

## Notes

- Every essay section now has its own folder under `sections/<section-slug>/`.
- Every covered section has a `metadata.jsonl` provenance file and `download-report.md`.
- Download errors are recorded inside metadata rows rather than hidden. They were Wikimedia 429 media throttles, not local script failures.
- The downloader is resumable: rerunning a section skips titles already recorded in `metadata.jsonl` unless `--overwrite` is used.

## Verification

```bash
python3 -m unittest discover -s video-essay-resources/tests
# Ran 11 tests: OK
```
