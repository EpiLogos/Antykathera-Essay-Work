# T17 local adoption and harness progress

Accepted remote head was resolved and matched locally at `347e53dd80a275da30df3e5605dc38c23f7118e1`, with a clean tree before editing. See `local-handoff.json` for stash identity, quilt hashes and protected NOTES hashes. The stash remains preserved and unapplied.

The intake helper now discovers every live quilt file, requires all 36 recovery packets to name that complete live corpus, records input hashes and actual source line anchors, and accepts the documented subcommand/root argument order. This mechanical preflight does not certify semantic recovery. Actual intake has not yet run: the 36-packet recovery barrier remains active.

Hygiene now requires reconciled canonical homes and registers, calls the actual target-taking `links` command, checks unresolved and frozen-legacy targets, and propagates effect-command failures. It reports global doctor debt separately. Heading strings and contribution IDs no longer impersonate canonical page identities.

Four functional tests pass against the real quilt corpus and real workspace commands, including anchor retrieval, rejection of discovery-only candidates, links/effects on the actual A01 home from outside the checkout, and failure propagation for an unresolvable target. Command: `python3 -m unittest discover -s tests -p test_p2_build_workflow.py -v`.

Baseline before canonical edits: source projections pass; three room projections are stale; doctor reports 3 dangling-room-fragment, 134 missing-register, 65 missing-status, 22 stale-bkmr-adapter, 65 thin-concept, 1 unresolved-link. The requested `dangling` command is absent from this checkout's CLI. These are recorded as inherited conditions, not P1 reopening. Targeted link checks use the supported `links <artifact> --json` command.

T17 remains in progress: depth acceptance, census reconciliation, target packets, the pilot, batch backcheck and final receipt have not yet completed. No manuscript composition or canonical enrichment is claimed by this checkpoint.
