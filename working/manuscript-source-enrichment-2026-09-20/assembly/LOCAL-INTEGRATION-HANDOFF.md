# Local integration handoff — whole-manuscript enrichment

Date: 2026-09-23
Repository: `EpiLogos/Antykathera-Essay-Work`
Branch: `codex/manuscript-source-enrichment-2026-09-20`

## Standing

The third relational pass is complete on the shared enrichment branch. The sovereign manuscript on main remains untouched pending authorial acceptance.

The verified assembly before this handoff is at branch head `949294799d80fca14656ecf0a190e32287972003`.

Primary assembled artifacts:

- `working/manuscript-source-enrichment-2026-09-20/assembly/THE-RETURN-OF-ZERO.md`
- `working/manuscript-source-enrichment-2026-09-20/assembly/THE-RETURN-OF-ZERO.html`
- `working/manuscript-source-enrichment-2026-09-20/assembly/WHOLE-PASS-REVIEW.md`
- `working/manuscript-source-enrichment-2026-09-20/assembly/SOURCE-COVERAGE.md`
- `working/manuscript-source-enrichment-2026-09-20/assembly/ASSEMBLY-MANIFEST.json`
- `working/manuscript-source-enrichment-2026-09-20/assembly/FINAL-VERIFICATION.md`

Verified content identities:

- Markdown Git blob: `a3b6c1b74ef158936ca5acc75431101ce9bd2a2d`
- Markdown SHA-256: `42e964ed7bdd5420b59743bbc69ccd96aae75c24d93e0834ed3bf06e40059549`
- HTML Git blob: `24441a7d3aa92eff1bcc39e15978059966c85b43`
- HTML SHA-256: `8504be7b5394fd7318a25846bd772d18933b319df857ceac81c00f2f7e459fb5`

The final candidate contains all 48 movements and 248 resolving note definitions. Browser checks, MathML rendering, internal links, whole/§5 views, reprise controls, notes, theme switching and mobile presentation were verified in the remote packaging run.

## Local action

Fetch the branch exactly. Do not merge it into main or overwrite `submission-package/essay/THE-RETURN-OF-ZERO.md` unless Frank explicitly accepts the candidate.

Recommended sequence:

```bash
git fetch origin codex/manuscript-source-enrichment-2026-09-20
git rev-parse origin/codex/manuscript-source-enrichment-2026-09-20
git show origin/codex/manuscript-source-enrichment-2026-09-20:working/manuscript-source-enrichment-2026-09-20/assembly/FINAL-VERIFICATION.md
```

Then materialise the branch in the existing repository using the project's normal minimal-worktree law. Prefer the existing manuscript workspace if it can safely inspect the remote-tracking branch; otherwise create one bounded temporary worktree for this branch only.

Verify the assembled Markdown and HTML against the hashes above. Open the HTML reader locally and confirm it renders without remote dependencies.

## Acceptance boundary

This is a model-composed candidate for Frank's judgment. Do not:

- silently promote it to the sovereign manuscript;
- alter the eight submitted section returns while fetching;
- erase the source-specific residual debts recorded in `SOURCE-COVERAGE.md`;
- publish optional first-person testimony that remains separately held;
- rerun broad prose generation merely because local formatting differs.

After fetch and verification, report:

1. local repository/worktree path;
2. fetched commit SHA;
3. Markdown and HTML hash verification;
4. whether the HTML opens correctly;
5. any local-only breakage or path issue;
6. the exact next authorial acceptance/promotion step, without performing it unless explicitly commissioned.
