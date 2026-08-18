# Local Markdown Wayfinder Tracker

## Wayfinding operations

- Maps live in `maps/` and carry `label: wayfinder:map`.
- Tickets live in `tickets/`. Their `parent` field names the map file, and their `label` is one of `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`.
- A ticket is open when `status: open`; it is closed when `status: closed` and has a matching resolution note under `research/` or a resolution comment appended beneath `## Resolution`.
- A session claims a ticket by filling `assignee` before doing any work. An open ticket with an empty `assignee` is unclaimed.
- `blocked_by` contains ticket filenames. A ticket is unblocked only when every listed ticket is closed.
- The frontier is the ordered set of open, unassigned tickets whose `blocked_by` list is empty or fully closed.
- The map indexes closed decisions by title and link under `## Decisions so far`; open tickets remain discoverable through their `parent` metadata and are not duplicated in the map body.
- New tickets are created first; dependency filenames are wired in a second pass.
- Research assets live under `research/` and are linked from the resolving ticket.
- Git/branch discipline follows the repository's live `AGENTS.md` and `WRITING-PROTOCOL.md`. Preliminary publication work currently occurs on `main`; model-written essay versions use the later ratified writing-branch protocol.

