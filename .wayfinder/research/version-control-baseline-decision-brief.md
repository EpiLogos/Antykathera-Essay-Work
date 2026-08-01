# Version-control baseline decision brief

**Ticket:** [Establish the version-control baseline](../tickets/001-establish-version-control-baseline.md)  
**Map:** [Complete Epi-Card v1 Runtime](../maps/complete-epi-card-v1-runtime.md)  
**Date:** 2026-08-01  
**Decision status:** Human authorisation required; no files have been staged or committed.

## Recommendation

Create the repository's root commit from an explicit Return of Zero and Epi-Card allowlist, not from the whole untracked working tree. The baseline should preserve the sovereign manuscript, canonical source houses, Frank-authored source notes, deterministic projections, project governance, submission specifications, and their real tooling/tests. It should leave the separate `definition-of-god-working/` tree, the copied `epi-logos-plugin-resources-copy-10-07/` tree, and the deliberate `essay-workshop/_to_delete/` queue untracked until Frank decides their repository ownership and, for the media corpus, confirms that the recorded rights/provenance support repository distribution.

This gives subsequent Wayfinder work a real `HEAD` without silently claiming every file that happened to be present in the workspace.

## Read-only findings

- The current branch name is `main`, but `git rev-parse --verify HEAD` fails: the repository has no commit.
- The working tree contains 1,692 files excluding `.git`; all project roots are untracked. `.bkmr/` and `.DS_Store` are ignored by the repository's two-line `.gitignore`. Some Python caches are ignored only by ambient/global rules and therefore need repository-local rules.
- The recommended baseline allowlist contains approximately 916 files and 14 MiB before Git compression at the time of this audit. It includes four preserved source-house `NOTES.md` files and the project symlinks; the final count must be recorded from the approved staged snapshot because active Wayfinder research may add files before authorisation.
- The whole workspace is approximately 101 MiB. There are 109 image/PDF assets totalling approximately 78.2 MiB. No video, audio, archive, or file over 10 MiB was found. The largest file is a 3.31 MB JPEG; the largest baseline binary is the 2.44 MB `essay-workshop/antykathera-resources/Antikythera_AGENTWORLD-Brief.pdf`. Git LFS is therefore not technically required for this first baseline.
- Six SQLite databases exist, all under ignored `.bkmr/db/`; AGENTS.md explicitly classifies BKMR databases as disposable.
- Thirty-four Python bytecode files and four `__pycache__` directories exist, plus `.pytest_cache/`. These are generated and should not enter the baseline.
- No environment file, private-key file, credential file, or certificate was found by filename. A high-confidence credential-pattern scan of non-Markdown source found only ordinary local variables named `token`, not embedded credentials. This is evidence, not a guarantee; the staged snapshot still needs a final secret scan.
- `ROOM.md`, `READING.md`, source indexes, the Epi-Card release validation reports, and `FILE_MANIFEST.sha256` are generated or derived, but they are intentional checked projections. The lifecycle hook runs their reproducibility/freshness checks, so they belong in the baseline alongside their generators.

## Exact inclusion policy

Stage only the following paths for the first commit:

```text
.gitignore
AGENTS.md
CLAUDE.md
Antykathera Concept Index.md
Antykathera Essay Work.md
refs-sources-args.base
.agents/
.claude/
.codex/
.wayfinder/
docs/
essay-workshop/
submission-package/
tests/
tools/
writing-guidance-tools/
```

Within that allowlist:

- Include `essay-workshop/THE-RETURN-OF-ZERO.md`, the central plan, orienting principles, all live nodes, canonical `SOURCE.md` houses, all four Frank-authored `NOTES.md` files unchanged, frozen provenance, active ideas, source projections, `ROOM.md`, and protected `READING.md` files.
- Include the complete `submission-package/epi-card-system-v1/` normative package: specifications, contracts, database schemas, API, examples, scripts, skill references, release manifests/reports, and UI declaration.
- Include `.wayfinder/` so the active map, tickets, and decision research survive the transition to branch-based work. The ticket/map statuses remain unchanged until Frank authorises and the root commit actually exists.
- Preserve symlinks as symlinks, including `.claude/skills/*` and the internal `AUTHORIAL-TEXT.md` link.
- Exclude ignored operating-system and Python cache files even when they sit inside an included directory.
- Exclude `essay-workshop/_to_delete/` from the initial index without deleting or ignoring it. Its name records unresolved human intent; keeping it visibly untracked is safer than either canonising or erasing it.

## Explicitly deferred from the first commit

| Path | Audit result | Baseline treatment |
|---|---|---|
| `definition-of-god-working/` | 158 files, about 77 MiB; a distinct manuscript/workstream with 109 total workspace media/PDF assets concentrated here, download metadata, provenance reports, and generated download/test outputs | Leave untracked. Decide repository ownership and audit distributable media rights before a later dedicated commit or separate repository. |
| `epi-logos-plugin-resources-copy-10-07/` | 98 files, about 4.6 MiB; explicitly named as a copy and outside the project-local skill authority | Leave untracked. Decide whether it is vendored source, reference-only material, or should be removed from this repository. |
| `essay-workshop/_to_delete/` | One consumed quilt fragment | Leave untracked and visible. Frank decides deletion, archival relocation, or inclusion. |
| `.bkmr/` | 488 generated retrieval adapters/database files, including six SQLite databases | Keep ignored and regenerate from canonical material. |
| `.pytest_cache/`, every `__pycache__/`, `*.pyc` | Local test/interpreter output | Ignore. |
| every `.DS_Store` | macOS metadata | Ignore. |

No excluded path should be deleted or moved as part of establishing `HEAD`.

## Exact `.gitignore` change

Replace the current two lines with this repository-local minimum:

```gitignore
# macOS metadata
.DS_Store
**/.DS_Store

# Disposable local retrieval state
.bkmr/

# Python-generated state
**/__pycache__/
*.py[cod]
.pytest_cache/
.coverage
coverage.xml
htmlcov/
.mypy_cache/
.ruff_cache/

# Local environments and secrets
.env
.env.*
!.env.example
.venv/
venv/

# Editor temporaries
*~
*.swp
*.swo
```

Do not add blanket patterns for `*.sqlite`, `*.db`, `*.pdf`, `*.jpg`, `*.png`, `ROOM.md`, `READING.md`, `dist/`, `build/`, `renders/`, or `*.epicard`. Those names can denote intentional portable databases, evidence, source media, deterministic projections, or release artifacts in this project. Runtime-specific generated directories should be ignored only after their exact workspace paths are fixed by implementation.

## Proposed staged batches

These are review batches for one root commit, not separate commits. Use explicit pathspecs; never use `git add .` or `git add -A` for this baseline.

### Batch 1 — repository governance

```sh
git add -- .gitignore AGENTS.md CLAUDE.md .agents .claude .codex
```

### Batch 2 — canonical essay and its projections

```sh
git add -- "Antykathera Concept Index.md" "Antykathera Essay Work.md" refs-sources-args.base essay-workshop ":(exclude)essay-workshop/_to_delete/**"
```

Before continuing, explicitly confirm that all four `NOTES.md` paths are staged and byte-identical to the working files. They are preservation targets, never edit targets.

### Batch 3 — Epi-Card and submission package

```sh
git add -- submission-package .wayfinder docs
```

### Batch 4 — real tooling, tests, and authoring guidance

```sh
git add -- tools tests writing-guidance-tools
```

After every batch:

```sh
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
git status --short
```

The final staged list must contain no path under `definition-of-god-working/`, `epi-logos-plugin-resources-copy-10-07/`, `.bkmr/`, `.pytest_cache/`, any `__pycache__/`, or `essay-workshop/_to_delete/`.

## Pre-commit evidence gates

Run these against the real staged snapshot:

```sh
git diff --cached --check
git diff --cached --name-only --diff-filter=ACMR
git diff --cached --numstat
git grep --cached -n -I -E 'BEGIN ([A-Z ]+ )?PRIVATE KEY|(^|[^A-Za-z])(api[_-]?key|client[_-]?secret|password)[[:space:]]*[:=]'
python3 tools/build-source-projections.py --project-root . --check
python3 tools/build-section-rooms.py --project-root . --check
python3 submission-package/epi-card-system-v1/scripts/validate-spec-package.py
python3 -m pytest
```

The credential scan returning no matches is the expected result. Any match must be reviewed without copying the suspected value into logs or chat. The deterministic projection checks, Epi-Card package validator, and real test suite must pass before the root commit is created. Record the staged file count and `git write-tree` result in the commit handoff so the exact approved snapshot is reproducible.

Proposed commit message:

```text
chore: establish Return of Zero project baseline
```

## Rollback and recovery

Because the branch is unborn, `git restore --staged` and `git reset HEAD` are not reliable pre-commit rollback instructions. To remove an accidentally staged path while preserving the working file:

```sh
git rm --cached -r -- path/to/accidental-entry
```

To clear the entire unborn index while preserving every working file:

```sh
git rm --cached -r -- .
```

Then repeat the explicit allowlist batches. Verify the working tree immediately with `git status --short`.

After committing:

```sh
git show --summary --stat HEAD
git status --short
git fsck --no-reflogs
```

If review finds an omission or accidental inclusion after the root commit, preserve the root commit and correct it with a new explicit follow-up commit. Do not rewrite or delete the root commit without a separate authorisation. The deferred trees should still appear as untracked in `git status --short`; that is deliberate evidence that they were not silently claimed.

## Required human authorisation

Frank must provide one explicit authorisation in substance:

> I approve the exact baseline allowlist and exclusions in `.wayfinder/research/version-control-baseline-decision-brief.md`; authorise the stated `.gitignore` edit; and authorise staging, validating, and creating the initial `main` commit with message `chore: establish Return of Zero project baseline`. The deferred `definition-of-god-working/`, `epi-logos-plugin-resources-copy-10-07/`, and `essay-workshop/_to_delete/` paths must remain untouched and untracked.

Until that authorisation is given, the correct state is the present one: research brief written, ticket open, no staged files, and no `HEAD`.
