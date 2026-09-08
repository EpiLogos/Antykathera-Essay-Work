# T22 — Room auditor recognises required P1 alignment

Changed only `tools/audit-room-depth.py`: added `P1-CANONICAL-ALIGNMENT.md` to ALLOWED and the required-file tuple. The room README line5 and its builder template at tools/build-section-rooms.py line460 explicitly state that each room contains generated ROOM.md and authored P1-CANONICAL-ALIGNMENT.md. All eight numbered rooms contain both. Optional learning, scratch and visual surfaces remain optional; existing content, unexpected-file, legacy, quotation, learning-route and generated-freshness checks remain unchanged.

Validation: `python3 -m unittest tests.test_audit_room_depth -v` — **4 tests passed**, including both real-room positive tests and both real mutation/rejection tests. An additional isolated copy of the actual 02-return-of-zero room with its P1 alignment removed was rejected by the actual audit_room function with `required file is missing: P1-CANONICAL-ALIGNMENT.md`. No mocked filesystem or graph was used. Scoped git diff whitespace check passes.

No prose, source, generated room, test file, protected material or index changes. No other global failures investigated. This receipt and the two-line auditor change are unstaged pending a grant.
