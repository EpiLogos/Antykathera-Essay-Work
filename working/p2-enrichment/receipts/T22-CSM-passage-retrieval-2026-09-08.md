# CSM passage retrieval repair — 8 September 2026

Completed the single owned source repair after full SOURCE and local-copy reading, resolver lookup and pre-write effects (no declared transverse threads). No sibling NOTES exists and none was created.

Added exact anchors `taylor-2026-antykathera-csm-lecture-notes-q001`, `-q002`, `-q003` before their existing headings, plus standalone Locator and Provenance fields for local-copy lines **33, 31 and 41**, respectively. Fifteen lines added, zero removed. Removing the recorded additions reconstructs the entire prior SOURCE byte for byte. Quotations, inherited prose, `claim_status: Argued`, `evidence_status: never-evidence`, dialogue-record typing and `citation_ready: false` remain unchanged. The local copy remains byte-identical.

The q002 card’s pre-existing “comptually” differs from “comptationally” in local-copy line31. The quotation was preserved exactly as requested; its added Provenance field discloses the difference and makes no transcription upgrade. q001 and q003 wording were checked against their exact local lines.

The actual `build-source-projections.py` parser now returns all three passage IDs with nonempty locators and provenance. Its current global count is **536**, closing the reported 533/536 gap on the Python side. No projection output was rebuilt by this task; parent owns source/BKMR rebuilding and the final equality test.

**Scoped SOURCE T22: 1 target, 0 failures.** Scoped `git diff --check` passed. No argument, consumer, other SOURCE, protected material or index write.

Canonical file: `submission-package/essay/symbolon/episteme/sources/internal-corpus/taylor/taylor-2026-antykathera-csm-lecture-notes/SOURCE.md`

Final SOURCE SHA-256: `72bcd416f3a47a31679fa3d71271c29042cb57cc1fc1a7be88642300ea1a3413`. Local-copy SHA-256: `c2666da92851b92c549ba754f6a94d320f11f36f46ad02fa8698fcc785d556c7`.

Exact additions and reconstruction proof, before snapshot, effects, parser output and T22: `working/p2-enrichment/snapshots/T22-private-CSM-passage-retrieval-2026-09-08/`. Adjacent JSON is the machine receipt. Released to parent; unstaged until explicit index grant.
