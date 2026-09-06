---
title: P2 Local Enrichment Launch
label: wayfinder:map
status: ready — remote-to-local handoff
created: 2026-09-06
programme_parent: "P2 Enrichment Handoff / T17 #18"
remote_branch: "origin/agent/t10-t16-p1-propagation"
local_branch: "agent/t10-t16-p1-propagation"
---

# P2 Local Enrichment Launch

## Purpose

Bring the accepted remote P1-complete branch into the user's local checkout **without losing any local work**, verify that local HEAD exactly matches the remote handoff, then execute T17/P2 enrichment on that branch.

This map supplements:

- `.wayfinder/maps/p2-enrichment-handoff.md`
- `working/final-argument-quilt-2026-08-23/P2-A01-A36-DEPTH-RECOVERY-CONTRACT.md`
- `.agents/skills/return-of-zero-build/SKILL.md`

## 1. Resolve the actual local repository

Do not assume an example absolute path from a skill file.

From the user's local Antykathera Essay checkout:

```bash
git rev-parse --show-toplevel
git remote -v
git status --short --branch
```

Confirm the repository is `EpiLogos/Antykathera-Essay-Work` and identify its real root.

## 2. Preserve local state before branch adoption

Never destroy uncommitted work or a divergent local branch tip just to make the handoff neat.

If the working tree is dirty, preserve it before switching:

```bash
if [ -n "$(git status --porcelain)" ]; then
  git stash push -u -m "pre-P2-handoff-$(date +%Y%m%d-%H%M%S)"
fi
```

Record the resulting stash reference in the execution receipt. Do **not** automatically pop that stash onto the P2 branch unless its contents are intentionally part of this work.

## 3. Fetch the accepted remote branch

```bash
git fetch origin --prune
git rev-parse origin/agent/t10-t16-p1-propagation
```

The remote ref is the live authority. Prompt-time SHAs are orientation only; always re-resolve the ref locally.

## 4. Create or reconcile the local tracking branch

If the local branch does not yet exist:

```bash
git switch --track -c agent/t10-t16-p1-propagation \
  origin/agent/t10-t16-p1-propagation
```

If it already exists:

```bash
git switch agent/t10-t16-p1-propagation
git fetch origin --prune
```

Then inspect divergence:

```bash
git status --short --branch
git log --oneline --decorate --left-right --cherry-pick \
  agent/t10-t16-p1-propagation...origin/agent/t10-t16-p1-propagation
```

### Existing local branch is only behind

Fast-forward it:

```bash
git merge --ff-only origin/agent/t10-t16-p1-propagation
```

### Existing local branch has local-only/divergent commits

Preserve the local tip before aligning:

```bash
SAFETY="safety/pre-p2-local-$(date +%Y%m%d-%H%M%S)"
git branch "$SAFETY" HEAD
git reset --hard origin/agent/t10-t16-p1-propagation
```

Record the safety branch name. The reset is allowed **only after** uncommitted work has been stashed and the divergent commit tip has been preserved by the safety branch.

Do not merge/rebase unknown local-only commits into the accepted P2 handoff merely to avoid making a safety branch.

## 5. Prove exact handoff before editing

```bash
LOCAL_HEAD=$(git rev-parse HEAD)
REMOTE_HEAD=$(git rev-parse origin/agent/t10-t16-p1-propagation)
printf 'local  %s\nremote %s\n' "$LOCAL_HEAD" "$REMOTE_HEAD"
test "$LOCAL_HEAD" = "$REMOTE_HEAD"
git status --short --branch
```

Start P2 edits only after the equality check passes and the working tree is clean.

Work **on `agent/t10-t16-p1-propagation` itself** unless the user explicitly requests another branch. Commit P2 work there in coherent receipts and push that same branch to `origin`.

## 6. Read the P2 authorities before queue construction

Read, in order:

1. `.wayfinder/maps/p2-enrichment-handoff.md`
2. `working/final-argument-quilt-2026-08-23/P2-A01-A36-DEPTH-RECOVERY-CONTRACT.md`
3. `.agents/skills/return-of-zero-build/SKILL.md`
4. `.agents/skills/return-of-zero-pages/SKILL.md`
5. `.agents/skills/return-of-zero-source/SKILL.md`
6. T17 / GitHub #18

The first substantive P2 operation is **not** blind `workflow.py intake`. It is recovery of the full authored depth axis A01–A36.

## 7. Mandatory argument-first depth recovery

Before bulk register dispatch:

- create `working/p2-enrichment/argument-depth/A01.md` through `A36.md` as working receipts;
- inspect the **live complete contents** of `submission-package/essay/quilt/`;
- for every Argument packet, record a yield or `no distinct yield` for every quilt file;
- read every materially implicated canonical `SOURCE.md` and sibling protected `NOTES.md` where present;
- privilege recoverable Taylor-authored signal over later AI resummarisation where provenance allows;
- never attribute mixed dialogue language to Taylor when speaker provenance is unclear;
- route recovered depth into the correct A/C/E/root/Matheme/Mytheme/Episteme office instead of expanding one page indiscriminately;
- send structural pressure through T22 rather than silently changing the canonical census.

Only after the A01–A36 packet set is present should the machine intake be reconciled and bulk page dispatch begin.

## 8. T17 intake after depth recovery

Use the real local root:

```bash
ROOT=$(git rev-parse --show-toplevel)
python3 .agents/skills/return-of-zero-build/workflow.py intake \
  --project-root "$ROOT" \
  --output intake.json
```

Reconcile `intake.json` against:

- T09 canonical census;
- P1 48-movement propagation;
- all candidate dispositions;
- the 36 A-depth packets;
- root / Matheme / Mytheme / Episteme record identities.

`intake.json` is a discovery aid, never the authority deciding what the field contains.

## 9. Pilot and onward sequence

T17 closes only after one ratified pilot demonstrates:

```text
A-depth recovery
→ target-keyed packet
→ canonical home
→ raw #0/#1/#2/#3/#4/#5→0 chassis
→ page-specific semantics
→ source / relation wiring
→ hygiene
→ Argument-depth backcheck
→ receipt
```

Then continue T18–T21 with the A-depth axis active under every register batch and T22 fold-back after each batch.

Do not begin manuscript composition before T24 accepts the developed world.

## 10. Push discipline

Commit coherent receipts frequently. Before each push:

```bash
git status --short --branch
git log -5 --oneline --decorate
```

Push the tracking branch:

```bash
git push origin agent/t10-t16-p1-propagation
```

Never force-push over remote work without an explicit authorial decision. If the remote branch advances during local execution, fetch and reconcile deliberately before pushing.