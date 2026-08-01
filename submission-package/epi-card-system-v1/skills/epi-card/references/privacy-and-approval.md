# Privacy, consent, and approval

## Disclosure classes

`secret`, `private`, `shared`, `public`.

Every row and asset has a class. `projection.materialize` creates immutable `private`, `shared`, `public`, or provider-specific snapshots from exact source revisions. `projection.validate` checks every included field and asset against consent, rights, and the selected disclosure profile. Every external request then records a `provider_disclosure_manifest` identifying the approved provider projection, provider/model, purpose, transmitted field paths/assets, retention expectation, and consent receipt. The public card reads an approved public projection; it never queries private records at display time.

## Pasu data

Use an immutable Pasu snapshot for each engagement. Attribute records state whether external-provider use is allowed. Raw session keys, private phrase references, precise birth/location data, and unredacted recordings must not appear in public URLs, QR targets, prompts, packages, or OKF files unless a narrowly scoped rule explicitly allows them.

## Required approvals

- QL frame approval after semantic validation.
- Canonical symbol approval.
- Art-direction/typography approval when marked canonical.
- Storyboard and plate acceptance.
- Final audio mix and final rendition approval.
- Shared/public print, OKF, and package approval.
- Publication approval, separate from render approval.

A revoked approval does not erase history; it blocks future use and marks affected renditions/publications according to retention policy. Sensitive payloads may be deleted or cryptographically erased while non-sensitive event facts remain.

## Locks

Locks are persisted at object or field path. Before changing semantic content, symbol geometry, palette, type, scene intent, accepted plates, tuning, render, or publication state, inspect active locks. A conflict is resolved only by an authorised `lock.release`; the agent must not claim or simulate an override.
