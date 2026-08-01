# Video Essay Resources

Working resource system for the video essay based on:

`../The Definition of God — Draft 3.md`

The directory is organised around the essay's sections. Images downloaded by the script land under:

`sections/<section-slug>/images/`

Each section also receives:

- `metadata.jsonl` — one source/license record per downloaded file
- `download-report.md` — human-readable acquisition notes

## Files

- `timeline-plan.md` — rough video sequence, symbols, and image needs
- `image-manifest.json` — curated visual brief and search queries per essay section
- `scripts/download_section_images.py` — Wikimedia Commons downloader
- `tests/test_downloader.py` — real parser/scoring/validation tests without network mocks

## Workflow

Preview candidates without downloading:

```bash
python3 scripts/download_section_images.py --dry-run
```

Download a small first pass for one section:

```bash
python3 scripts/download_section_images.py --section edge-of-the-rational --per-query 2
```

Download the full manifest:

```bash
python3 scripts/download_section_images.py --per-query 3
```

If a section returns too little, lower the threshold deliberately:

```bash
python3 scripts/download_section_images.py --dry-run --section edge-of-the-rational --min-score 5
```

The script uses the Wikimedia Commons API, not scraped search pages. It records canonical source URLs, author fields, licenses, MIME types, dimensions, and the exact query that found each file. This does not replace human visual selection, but it gives the selection process a trustworthy floor: known provenance, reusable licensing, and source metadata kept beside the files.

## Curation Rule

Keep only images that can survive direct contact with the prose. If an image merely says "mystical", "ancient", or "sacred" in a generic way, remove it. The strongest images here should carry a specific operation: limit, refraction, fall, minus sign, quotient, torus, Ma'at, anamnesis, Maya/code, or Epi-Logos.
