# CLI reference

## Global form

```text
epicard <domain> <action> [options]
```

Global options:

```text
--json | --jsonl
--request @file.json
--session <uuid>
--engagement <uuid>
--idempotency-key <value>
--dry-run
--resume <run-uuid>
--wait
--output <path>
```

Machine output goes to stdout. Logs go to stderr. No prompt is permitted unless `--interactive` is explicitly supplied.

Principal commands:

```text
epicard session open|resume|close
epicard engage create|inspect
epicard source ingest
epicard recording ingest|transcribe
epicard projection materialize|validate
epicard attractor create|resolve|revise
epicard ql initialize|map|reconcile|validate|approve|inspect
epicard lock acquire|release
epicard resonance resolve|project|compare
epicard symbol search|propose|generate|transform|canonicalize|validate|approve
epicard storyboard plan|revise
epicard image collect|generate|edit|alpha
epicard video submit|poll|continue|edit
epicard plate accept
epicard audio palette|render|analyze|mix|validate-loop
epicard compose render
epicard validate engagement|rendition|package
epicard poster select
epicard card render-web|render-print|package
epicard okf export|validate
epicard publish prepare|approve|execute|poll
epicard return deposit
```

Exit codes: `0` success; `2` request/schema; `3` permission/disclosure/auth; `4` state/idempotency conflict; `5` external provider; `6` retryable; `7` approval/review required; `8` cancelled; `9` internal runtime.
