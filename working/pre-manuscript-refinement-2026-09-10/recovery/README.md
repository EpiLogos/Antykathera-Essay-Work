# R2.1 original recovery — 12 September 2026

**Custody, not admission.** Four exact files from the unfinished R2.1 batch survive here. The remaining 58 authored postimages have not been recovered. Do not turn the old return's description of its local working tree into a statement about current `main`, fill the missing records from its summaries, or advance the R3–R6/T26 gates on the strength of this recovery.

## Exact surviving work

| Original file | Bytes | SHA-256 |
|---|---:|---|
| `S-World-and-Life.md` | 12761 | `2d1abf89818065d5e0d424c28cccbcf0445a85f4fe6ba2d2d6cb2ab446fae225` |
| `S1-Actuation.md` | 36605 | `ef4e2b59acb3f15fe0eda502042c421209086131aa1f49758f731c0d1115b2c7` |
| `R2-PRODUCT-ALLOCATION.md` | 10633 | `727815076de1754ff59ad90c7532d364988131b9ef938a764034298aa8905e1c` |
| `R2-PRODUCT-RETURN.md` | 13994 | `def06790bd5be55ab5a32c300a5f5d54e4c0fe445b5afaee36f9470d85a2c813` |

All four were recovered from the prior session's Library attachments and match the original transfer manifest. Their bytes, including their original relative links and status claims, are unchanged under `originals/<filename>.original`. The extra suffix prevents these noncanonical survivors from entering Markdown discovery as duplicate live S/S1 records. Relative links still describe the intended original homes; those homes and every expected hash are recoverable through the verifier. This directory is not a new canonical product home.

The first fragment at `../batches/R2.1/01.xz64part`, committed in `6051a9cb9843991ea5117218a1a22ca9dfe8c3aa`, decompresses only to a JSON-manifest prefix. It contains the complete 62-entry authored preimage/postimage tables, but no actual patch content; the compressed stream is incomplete. Its original full patch hash is:

`0907e6ef3e60c71f384eec010b413d2a9b61bfd7fa2c6e7267a72dad4e648514`

The original batch starts from `13b43fe290ee3dbc1d6686709f2e7bc4e7158292`, tree `48926879976a1161ef8b63bc7ca0fa3db7587589`. Live main was recovered at `20ebd6f34b1ef7e322259305e242dd75402538ec`, tree `3961567571edcc7f57dc9df27cc3436ba54bbab3`, through source artifact `10267797216` of workflow run `34609302695`. The artifact's repository archive SHA-256 was `ef847c6d89eec54ad5e378eb4dea8535c0b355c4ff990a42b54b78dde1ed0d02`; its reconstructed Git tree matched exactly. The sole branch and empty #26 comment thread supplied no remaining payload.

## Verify without promoting

From the repository root:

```sh
python3 working/pre-manuscript-refinement-2026-09-10/recovery/verify-recovery.py --output /tmp/r2-custody.json
python3 working/pre-manuscript-refinement-2026-09-10/recovery/verify-recovery.py --require-complete --output /tmp/r2-incomplete.json
```

The first command verifies original custody and emits all original hashes, the four survivors, the 58 missing postimages, and any current preimage conflicts. The second deliberately exits 2: this recovery cannot satisfy complete-batch admission. Exit 0 from custody verification never signifies a complete original archive or semantic acceptance.

Missing bodies include S0 Central, S2 AIKit, S3 Software Factory, S4 Workcell and S5 Quaternal Logic; the rewritten M37–M42 movements; their source, reciprocal, plan and tooling changes; and the R1 grounding, S admission and technical-preservation receipts. Existing pre-batch versions are not the missing postimages. The complete original archive/remaining fragments or original files matching the pinned hashes are required before resuming the original guarded admission.

## Baseline repair is a separate operation

The restored `20ebd6f` validation artifact ran 115 tests with three stale-projection failures and one unavailable-AIKit skip. Regenerating the three native surfaces locally changed 66 generated files; the full rerun then passed 115 tests with the same one skip. All 472 protected files and the entire A/C remained unchanged. These are baseline results, not the prior R2 working tree's 125-test or 144/288-record claims.

The accompanying bounded recovery workflow independently checks custody and original preimages, runs the real builders, complete current suite, freshness checks, all eight explicitly named rooms and C41 effects, and retains reader/pre-manuscript reports without treating report generation as semantic approval. It refuses any non-generated mutation and verifies the 472 protected files plus A/C byte-for-byte. Only that validated generated tree may fast-forward `main`, without force; concurrent advancement fails rather than being overwritten. Its artifact records actual command results, tested tree and publication SHA. No result is assumed in advance.

The existing map, R1/R2 tickets and all 62 authored preimages are deliberately left unchanged. The baseline repair does change generated preimages: the original full patch may therefore need separation into its hash-verified authored and generated paths before application. Preserve the original payload and its full-patch hash; admit only the exact authored postimages against their retained preimages, then regenerate and validate the derived surfaces with the recovered batch's tools. Never waive an authored conflict or rewrite a missing body. #26 carries the current recovery boundary. Independent R2 review, full R3/R4 field and movement work, R5 cold review and R6 common-base preparation remain unfinished. No sovereign manuscript or model-writing branch is started.

## Published baseline validation

Recovery commit `63e7a06bbb38a32acf0d525ba02ba86e9e64bf3f` was followed by validated baseline commit `4d8cf138bd141a16e0ae40b9648888f1fd149f74`, tree `91228bc8be8e4e932bb98f04f9b0840ba3fe587d`. GitHub run `34667433387` passed: **115 tests, 114 passed and one expected skip**, all three freshness checks, all eight rooms and C41 effects. All 472 protected hashes and the entire A/C matched. The live census remains **137 shared / 281 admitted**. The generated-only repair changed 66 files.

`BASELINE-VALIDATION.json` retains the publication and artifact identities and scope. Artifact `10289614001` was downloaded and its SHA-256 verified before its generated patch was used to reconstruct the exact published Git tree locally. The original local baseline differs only in 278 absolute checkout-root prefixes in generated `reader-audit.json`; replacing that root makes the files byte-identical, and every other file agrees exactly. This is diagnostic path variation, not a change to authored content. The receipt and this README clarification are documentation-only additions after the tested baseline commit; they do not claim a new full-suite run on their own later commit.
