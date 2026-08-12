---
name: return-of-zero-orient
description: Use when a Return of Zero task needs project orientation, canonical retrieval, argument traversal, context assembly, effect mapping, or recovery of a live manuscript location.
---

# Orient Return of Zero Work

Read `AGENTS.md`, then run:

```bash
python3 tools/okf-workspace.py --project-root . status --json
```

Ordinary conversation can remain in chat. When canon becomes relevant, read `return-of-zero-orienting-principles.md`, then use `find`, `open`, `context`, `trace`, and `effects` from `okf-workspace.py` at the grain the task requires. An index, room, or search hit locates authority; reopen the canonical body.

Recover a record's **register** from its frontmatter (`symbolon`, `matheme`, `mytheme`, `episteme`, or a declared cross-register composition) before traversing it, and carry that register in the context receipt. Register is the admission-and-return channel, not a filing label: a movement or argument declares the register composition it admits and carries, and records outside the essay return to exact essay locations. A record with no declared register is an unratified-register-census debt: name it as a debt, never assume a register from folder placement. `status --json` reports the register census; `find --register <name>` filters by declared register.

The publication sixfold is fixed, and the publication body has one home: `submission-package/essay/`. `#0` the rooms (`submission-package/essay/section-rooms/` — movements as the `1`s, arguments as the `0`), `#1`–`#4` Symbolon / Matheme / Mytheme / Episteme (`submission-package/essay/symbolon/`), `#5` the sovereign essay. The field infers into the rooms; the rooms structure the essay; the essay returns the whole. Concept nodes and the recovered `reference-notes/` shelf live in `submission-package/essay/symbolon/episteme/concepts/`; paths in `submission-package/essay/symbolon/episteme/maps/`.

Before changing a declared transverse thread, read the whole path and run `effects`; never infer a relation from shared vocabulary. For native QL notation, recover the core theorem spine and whole eight-determination field before mapping another register. `X/x` is authorial QL notation; never call the relation Jungian. Never introduce a strawman to make an established position appear newly won.

Active ideas are optional deliberate continuity, not a work ledger:

```bash
python3 tools/project-agent-harness.py ideas list --json
```

Read [workspace-contract.md](references/workspace-contract.md) when changing schemas, authority rules, retrieval adapters, or generated surfaces.
