---
title: Repair the lenses register — Baudrillard/Foucault homed, MEF lenses surfaced
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: lenses-agent-2026-09-25
blocked_by:
  - 028-migrate-canonical-suite-into-section-rooms.md
created: 2026-09-25
---

# Repair the lenses register — Baudrillard/Foucault homed, MEF lenses surfaced

## Question

`symbolon/episteme/lenses/` promises MEF lenses in its README but holds only `baudrillard.md` (record_id `lens-baudrillard`, no source linkage at all) and `foucault.md`. Frank's direction: return the two files to their correct source houses, surface their influence properly, and make the register actually hold MEF lenses.

1. `baudrillard.md`: absorb its developed lens reading into the `baudrillard-1976` source house (under `episteme/sources/` — resolve the exact path with `tools/source_resolver.py`, never assume nesting depth). Influence surfaces as declared source relations in the house's consuming records — never as Baudrillard endorsing the essay's inference. Then either replace the lens record with one declaring proper `source_ids`, or retire the file to `working/_to_delete/2026-09-25-retire/` if the house now carries the content — state which and why.
2. `foucault.md`: same treatment against `foucault-1976` (it already declares `source_ids` including `taylor-2026-mef-twelve-lenses`).
3. Build the MEF lens records the README promises from the internal-corpus house `episteme/sources/internal-corpus/taylor/taylor-2026-mef-twelve-lenses/`: the twelve lenses as twelve declared lens records in `lenses/` (or one index record + twelve sections if the house's own structure says so — follow the house). Nothing is invented: the records carry the house's own content and declared structure, with provenance pointers back to it.
4. Update `lenses/README.md` to describe what the register now actually holds.
5. Sweep nodes that cite the two lens files by path; repoint to the houses/records.

Conduct: propose-don't-overwrite; source-house `<source_id>-NOTES.md` files are never touched; no commits; no builders.

Report → `.wayfinder/research/029-lenses-report.md`: what was homed where, the twelve-lens structure chosen, links repointed, anything stopped.

## Resolution

Lens readings homed verbatim in both source houses (anchors preserved); 32 body links + 6 house frontmatter entries repointed; both stray files retired; twelve MEF lens records built from the taylor-2026-mef-twelve-lenses house (SHA-verified); register README rewritten. Report: ../research/029-lenses-report.md
