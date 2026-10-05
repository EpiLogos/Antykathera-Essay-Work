# The Return of Zero — whole-manuscript candidate

The third relational pass over the eight source-led section submissions. Model-composed candidate for Frank G. Taylor's judgment; authorial acceptance remains open.

- [HTML reader](THE-RETURN-OF-ZERO.html)
- [Canonical editable Markdown](THE-RETURN-OF-ZERO.md)
- [Exact before/after changes and common-method counts](WHOLE-PASS-CHANGES.html)
- [Performed whole-pass review](WHOLE-PASS-REVIEW.md)
- [Source coverage and remaining publication limits](SOURCE-COVERAGE.md)
- [Assembly manifest](ASSEMBLY-MANIFEST.json)
- [Structural checks](CHECKS.json) and [preservation checks](SEMANTIC-CHECKS.json)

Open the HTML as a local file for the complete reader. The whole work is the default. **Read §5 alone** shows the same canonical section with its grounding, lens and narrative reprises expanded. **Expand reprises** also makes those passages available within the full work. Notes keep stable whole-manuscript numbering in both views. The reader requires no remote script or font service.

All eight submitted sections remain untouched under `../sections/`. Baselines, native sources, the sovereign manuscript and main remain unchanged. The exact input head is `19a1d5d58a104ed27359d952aff6e7edc781816a`; native source authority is `26e42cbbbaa795ecc7dcc480a10c40393f5a8352`.

The historical `ADMISSION-CHECK-2026-09-21.md` records an earlier missing-s1 checkpoint, not the current admission. The complete s1 is included in this assembly. s4's wider archival-audit limits remain visible rather than being converted into a claim of exhaustive reading. Personal testimony and unapproved exact first-person excerpts remain in the section publication-option files.

## Reproduction

The build consumes the exact eight source files, refuses hash drift, applies the explicit `editorial_revisions.py` operations and generates the Markdown before rendering it. `WHOLE-PASS-EDITS.json` retains every old/new passage. The final MathML cache permits subsequent builds without a network dependency.

```sh
python3 -m pip install mistune==3.2.1
python3 working/manuscript-source-enrichment-2026-09-20/assembly/build_whole_pass.py
python3 working/manuscript-source-enrichment-2026-09-20/assembly/verify_whole_pass.py
```

To regenerate the MathML cache itself, use KaTeX 0.16.22 and set `ROZ_KATEX_MODULE` to its installed module path. Only static MathML is incorporated into the reader; font binaries are not distributed. Preservation tests concern textual identity, notation and source pins, not independent proof of every claim in the essay.
