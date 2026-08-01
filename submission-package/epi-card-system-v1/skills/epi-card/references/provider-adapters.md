# Provider adapter rules

Every external provider/model/version is described by a `provider-capability.schema.json` record checked on a known date. The adapter validates the plan against that record before submission.

A provider request stores:

- operation and model version;
- exact structured prompt/instruction;
- input/reference asset hashes and roles;
- duration, aspect, resolution, seed when available, and safety/options;
- disclosure manifest;
- provider job ID, raw response, and resume cursor.

Seedance 2.0 is the reference first video adapter. Allocate references deliberately; do not assume all providers share its limits or editing/continuation features. Use the capability record, not remembered limits.

Provider output states map into runtime states without deleting the native provider response. Failed or timed-out requests resume by provider job ID. A new request is used only when the old job is terminal or the request itself changes.

Never include secret content. Private content requires explicit consent and provider permission. Provider-generated assets remain candidates until accepted.
