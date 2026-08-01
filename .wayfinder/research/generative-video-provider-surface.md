# Generative-video provider surface for Epi-Card v1

Checked: 2026-08-01 (Europe/London)

## Resolution

Generative video is a plural, optional acquisition lane. It must not be a release prerequisite and it must not be conflated with public/licensed image and video procurement. A conforming card can obtain its plates from public media, imported or commissioned assets, or a generative provider; deterministic composition remains responsible for exact symbols, typography, interaction timing, audio placement, safe frame, and loop behaviour.

The immediately usable reference route is **Seedance 2.0**, either directly through BytePlus ModelArk or through Runway's provider API. **Seedance 2.5 must not yet be registered as callable**: BytePlus has an official product page describing it as “coming soon,” but no official production API reference, model ID, authentication contract, pricing table, or job lifecycle could be verified. Its registry status should be `announced`, `active: false`, until an adapter health probe succeeds against an official endpoint. [BytePlus Seedance 2.5 page](https://www.byteplus.com/en/contact-us/ai-seedance2-5-official)

The strongest current provider-independent alternatives are Google Veo 3.1 and Runway Gen-4.5. Amazon Nova Reel 1.1 remains useful for long, storyboarded 720p output and content credentials, but its family has a legacy/EOL signal in current Bedrock documentation and therefore needs a lifecycle probe before use. OpenAI's Sora 2 API is not a viable new dependency: it is deprecated and scheduled to shut down on 2026-09-24. [OpenAI video-generation guide](https://developers.openai.com/api/docs/guides/video-generation)

## Production surfaces

### 1. BytePlus ModelArk — Dreamina Seedance 2.0

**Callable surface.** `POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks`, authenticated with a ModelArk API key, returns an asynchronous task ID. The public regional endpoint documented by BytePlus is `ap-southeast-1` (Johor); activation and credentials are region-isolated. [Create-video API](https://docs.byteplus.com/en/docs/modelark/1520757) · [regional availability](https://docs.byteplus.com/en/docs/ModelArk/2191806)

**Exact current models.** `dreamina-seedance-2-0-260128`, `dreamina-seedance-2-0-fast-260128`, and `dreamina-seedance-2-0-mini-260615` are documented. Full Seedance 2.0 accepts text-only generation and multimodal reference generation with up to nine images, three videos, and three audio clips. Audio cannot be supplied alone; at least one reference image or video is required. Reference-video and reference-audio totals are each limited to 15 seconds. [Seedance 2.0 tutorial](https://docs.byteplus.com/api/docs/ModelArk/2291680) · [create-video API](https://docs.byteplus.com/en/docs/modelark/1520757)

**Output envelope.** Full Seedance 2.0 supports integer durations from 4–15 seconds or `-1` for model-selected duration; 480p, 720p, 1080p, and 4K; ratios `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, or adaptive. Fast and Mini stop at 720p. The full model alone supports 4K, encoded as 10-bit H.265/HEVC. Seed control and `camera_fixed` are not supported for Seedance 2.0. [Create-video API](https://docs.byteplus.com/en/docs/modelark/1520757)

**Operations and audio.** Official documentation describes generation, editing, and extension through multimodal reference requests. First-frame and strict first/last-frame image roles are supported. `generate_audio` controls synchronized voice, sound effects, and background music and defaults to true. The API does not document a structured shot-list output contract, so `multi_shot` should not be inferred merely from prompt expressivity; represent it as unsupported or unverified until a structured operation is documented and probed. [Create-video API](https://docs.byteplus.com/en/docs/modelark/1520757)

**Job lifecycle.** Create is asynchronous; clients can poll the retrieve endpoint or supply `callback_url`. Callback states are `queued`, `running`, `succeeded`, `failed`, and `expired`, with three delivery retries after a five-second acknowledgement failure. Task records live for seven days; generated video URLs are valid for only 24 hours and must be copied into Epi-Card's content-addressed storage immediately. [Retrieve-task API](https://docs.byteplus.com/en/docs/ModelArk/1521309) · [Seedance tutorial and output retention](https://docs.byteplus.com/api/docs/ModelArk/2291680)

**Policy and provenance.** Direct uploads containing real human faces are restricted. BytePlus documents trusted same-account outputs, preset digital characters, and an invited authorized-real-person asset library as separate paths. A visible “AI Generated” corner watermark is optional (`watermark`, default false); no cryptographic content credential is documented on the reviewed API pages. The runtime therefore must preserve its own immutable provider receipt: exact request, provider task ID, raw responses, usage, downloaded-output hash, and disclosure/rights records. [Create-video API](https://docs.byteplus.com/en/docs/modelark/1520757) · [private real-human asset library](https://docs.byteplus.com/en/docs/modelark/2333589) · [BytePlus terms index](https://docs.byteplus.com/en/docs/ModelArk/Terms_and_Conditions)

**Cost.** Billing is token-based and varies by output resolution and whether a video is supplied as input. As of the check date, full Seedance 2.0 online rates are documented as USD per million tokens: 480p/720p `7.0` without video input or `4.3` with video input; 1080p `7.7`/`4.7`; 4K `4.0`/`2.4`. Token consumption depends on input/output duration, dimensions, and frame rate, so the registry must retain the rate basis and formula rather than pretending this is a stable per-second tariff. [BytePlus ModelArk pricing](https://docs.byteplus.com/docs/ModelArk/1099320)

### 2. Runway API — hosted Seedance 2.0 and Gen-4.5

**Callable surface.** Runway exposes bearer-key endpoints for text-to-video, image-to-video, and video-to-video under `https://api.dev.runwayml.com/v1`, with the required version header `X-Runway-Version: 2024-11-06`. It currently lists `seedance2`, `seedance2_fast`, `seedance2_mini`, and `gen4.5`. [Runway API reference](https://docs.dev.runwayml.com/api/) · [setup](https://docs.dev.runwayml.com/guides/setup/)

**Hosted Seedance.** Runway documents text, image, and video input; keyframe, reference-image, reference-video, and generated-audio support; and 4–15 second output. `seedance2` spans 480p, 720p, 1080p, and 4K across 24 documented dimensions. Fast and Mini support 480p/720p. This is a credible first adapter when one API is preferable to managing ModelArk activation and regional assets. [Runway changelog](https://docs.dev.runwayml.com/api-details/api_changelog/) · [input profiles](https://docs.dev.runwayml.com/assets/inputs/)

**Gen-4.5.** Gen-4.5 is a narrower independent alternative: text-to-video and first-frame image-to-video, 2–10 seconds, with landscape/portrait text-to-video and a wider set of image-to-video shapes. No native audio, continuation, or Gen-4.5 video-edit operation is documented. It is useful for ordinary short plates, not as a semantic substitute for Seedance's multimodal editing surface. [Gen-4.5 guide](https://docs.dev.runwayml.com/guides/using-the-api/) · [input profiles](https://docs.dev.runwayml.com/assets/inputs/)

**Job lifecycle.** Submission returns a task ID. Poll `GET /v1/tasks/{id}` at intervals of five seconds or more with jitter and exponential backoff until `SUCCEEDED`, `FAILED`, or `CANCELED`; `THROTTLED` is queue-like. Output URLs expire within 24–48 hours and must not be exposed directly to users. No completion-webhook contract was found in the reviewed official API documentation. [Runway SDK/task lifecycle](https://docs.dev.runwayml.com/api-details/sdks/) · [output retention](https://docs.dev.runwayml.com/assets/outputs/)

**Policy and provenance.** Runway moderates inputs and outputs. Moderated generations cost the same as successful generations, repeated moderated requests can suspend an account, and safety failures must not be retried. Runway requests UI attribution as “Powered by Runway.” No C2PA/SynthID or other provider-signed provenance mechanism was documented on the reviewed official pages, so Epi-Card's own raw-response and hash receipt remains mandatory. [Content moderation](https://docs.dev.runwayml.com/api-details/moderation/) · [task failures](https://docs.dev.runwayml.com/api-details/task-failures/) · [attribution](https://docs.dev.runwayml.com/usage/attribution/)

**Cost.** One Runway credit is USD $0.01. Current rates are: `seedance2` 36 credits/s at 480p/720p, 40 credits/s at 1080p, 150 credits/s at 4K; `seedance2_fast` 29 credits/s; `seedance2_mini` 16 credits/s with a 64-credit minimum; `gen4.5` 12 credits/s. Persist the quoted price snapshot and the provider's realized usage response. [Runway pricing](https://docs.dev.runwayml.com/guides/pricing/)

### 3. Google Cloud — Veo 3.1 family

**Callable surface.** `veo-3.1-generate-001` and `veo-3.1-fast-generate-001` are documented as GA in `us-central1`; Vertex/Agent Platform requests use Google Cloud authentication and a long-running prediction operation. SDK examples poll the operation and can return bytes or write to a caller-owned Cloud Storage bucket. [Veo 3.1 model page](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate) · [first/last-frame API example](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-first-and-last-frames)

**Output envelope and operations.** The GA models support text-to-video, image-to-video, first/last-frame control, reference assets, and extension. Outputs are 4, 6, or 8 seconds at 24 FPS, `16:9` or `9:16`; the main model lists 720p, 1080p, and 4K, while Fast lists 720p/1080p. Up to four outputs can be requested. Content Credentials (C2PA) are explicitly supported, and Google also documents SynthID watermarking for Veo. [Veo 3.1 model page](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate) · [Google DeepMind Veo safety/provenance](https://deepmind.google/models/veo/)

**Audio documentation conflict.** Google's current API reference and pricing surface include a `generateAudio` mode and separate video-with-audio tariffs, while the current Veo 3.1 model page says sound generation is not supported for the GA Generate/Fast entries and supported for the Lite preview entry. Do not resolve this by family-name inference. Store audio as an output-profile-level capability and require a successful endpoint/model probe before selecting it. [Veo API reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation) · [Veo 3.1 model page](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate) · [Google pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)

**Policy and cost.** The request surface provides people/face controls such as `allow_adult` and `disallow`, and blocked requests or outputs are governed by Google's generative-AI policies. Current list pricing distinguishes audio and silent output: Veo 3.1 is $0.40/s with audio or $0.20/s silent at 720p/1080p (higher for 4K); Fast is $0.10–$0.12/s with audio or $0.08–$0.10/s silent at 720p/1080p. Because current consumption modes and audio statements conflict across official pages, the adapter must bind a price quote to the exact endpoint and output profile it successfully probes. [Google pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) · [first/last-frame parameters](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos-from-first-and-last-frames)

### 4. Amazon Bedrock — Nova Reel 1.1

**Callable but lifecycle-sensitive.** `amazon.nova-reel-v1:1` supports text-to-video and first-frame image-to-video, including automated or manually storyboarded videos in six-second increments up to two minutes. Output is fixed at 1280×720, 24 FPS, with no documented native audio, source-video editing, or continuation operation. Version 1.1 is documented only in `us-east-1`. [Nova Reel generation](https://docs.aws.amazon.com/nova/latest/userguide/video-generation.html)

**Execution and receipts.** Bedrock uses IAM/API-key credentials and `StartAsyncInvoke`; output must target caller-owned S3. `GetAsyncInvoke` supplies status. The result folder contains `manifest.json`, `video-generation-status.json`, `output.mp4`, and individual shot files, making it especially strong for durable execution receipts. Nova Reel 1.1 output carries verifiable Content Credentials unless its metadata is stripped. [Access and lifecycle](https://docs.aws.amazon.com/nova/latest/userguide/video-gen-access.html) · [Nova Reel generation/provenance](https://docs.aws.amazon.com/nova/latest/userguide/video-generation.html)

**Caution.** Bedrock's current model card marks Nova Reel as legacy in some regions and gives a 2026-09-30 EOL date for the documented v1 surface, while the Nova guide still calls v1.1 active. Register it as `lifecycle_check_required`, not as a default, and probe model availability immediately before scheduling. The reviewed official pricing page did not yield a stable machine-readable Reel rate, so store a live quote/billing lookup rather than hard-code a guessed price. [Bedrock model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-reel.html) · [Nova model list](https://docs.aws.amazon.com/nova/latest/userguide/additional-resources.html)

### 5. OpenAI Sora 2 — migration-only, not selectable for new Epi-Cards

Sora 2 and Sora 2 Pro can currently generate synchronized-audio clips from text or a first-frame image, extend completed videos, and edit existing generations through asynchronous jobs with polling or webhooks. However, the full Videos API and all Sora 2 model IDs are deprecated and will shut down on 2026-09-24. Existing jobs may be migrated through a temporary adapter, but new runtime plans must reject it. [OpenAI video-generation guide](https://developers.openai.com/api/docs/guides/video-generation) · [Sora 2 model page](https://developers.openai.com/api/docs/models/sora-2)

## Proposed capability-registry matrix

The present `provider-capability-1.0.0` record is a useful semantic summary, but it cannot safely select a production job. In particular, one scalar duration range cannot express discrete values, extension limits, operation-dependent limits, or resolution/audio price profiles; booleans cannot represent `unknown`, `preview`, or contradictory documentation; and it has no lifecycle, auth, polling, provenance, or billing contract.

Retain the current top-level identity and disclosure fields, then add the following versioned structures:

| Registry group | Required fields | Why it is needed |
|---|---|---|
| `availability` | `status` (`ga`, `preview`, `deprecated`, `announced`, `unverified`), `active`, `access_mode`, `regions`, `sunset_at`, `official_docs`, `last_document_check`, `last_probe_at`, `probe_result` | Prevents announced Seedance 2.5 or near-EOL Sora/Nova models from being selected. |
| `endpoint` | `base_url`, `submit_operation`, `auth_scheme`, `credential_ref_kind`, `api_version`, `sdk_version` | Makes the adapter invocation reproducible without storing secrets. |
| `input_profiles[]` | operation, modality combination, roles (`first_frame`, `last_frame`, `reference`), count/size/duration/format limits, face/person restrictions | Avoids treating text, first-frame, multimodal-reference, and source-video editing as interchangeable. |
| `output_profiles[]` | operation, allowed duration values or min/max/step/auto, dimensions/ratios, resolution, FPS, codec/container/bit depth, `native_audio`, `alpha`, max extensions and total duration | Lets planning choose an exact supported profile and catches documentation conflicts at the profile level. |
| `execution` | async flag, provider status map, poll endpoint/minimum interval, backoff/jitter, callback/webhook contract, cancellation, task-record TTL, output-URL TTL, retryable/terminal codes, provider idempotency support | Makes `video.submit`/`video.poll` resumable without duplicate paid generations. |
| `billing` | currency, unit basis, rates by exact output profile, minimum charge, moderation/failure billing, quote URL, checked time, provider-reported usage fields | Represents token formulas, credit tariffs, and per-second pricing without forcing them into one false common unit. |
| `provenance` | task/job ID, raw-request and raw-response capture, model ID/version, input hashes/rights refs, output hash, usage/cost, visible watermark setting, `c2pa`, `synthid`, provider-manifest refs, generated-at | Separates provider evidence from Epi-Card's immutable local receipt and retains public-media rights lineage. |
| `policy` | terms/AUP snapshot refs, moderation scope, people/faces, public figures, copyrighted characters/music, data retention/training statement, attribution, safety-failure retry rule | Makes provider choice and disclosure review explicit before data leaves the runtime. |
| `health` | last successful conformance probe, tested request fixture, observed response shape, download/hash result, drift reason | Official documentation is necessary but insufficient where product pages conflict; runtime selection should require a passing probe. |

### Candidate rows as of 2026-08-01

| Adapter/model | Status | Inputs | Output | Continue/edit | Native audio | Provider provenance | Execution | Cost basis | Default eligibility |
|---|---|---|---|---|---|---|---|---|---|
| BytePlus `dreamina-seedance-2-0-260128` | GA/callable after activation | text; 0–9 image; 0–3 video; 0–3 audio (audio not alone) | 4–15s; 480/720/1080/4K; six ratios + adaptive | both documented via references | yes | optional visible watermark; local receipt required | async poll + callback; task 7d; URL 24h | variable USD/M output tokens | eligible after credential + live probe |
| Runway `seedance2` | callable | text/image/video; keyframes and references | 4–15s; 480/720/1080/4K | video-to-video/reference controls; extension semantics must be profiled | yes | no signed mechanism documented; local receipt required | async poll; URL 24–48h | credits/s by resolution | eligible after credential + live probe |
| Runway `gen4.5` | callable | text or first-frame image | 2–10s; 720-class profiles | no / no | no | no signed mechanism documented; local receipt required | async poll; URL 24–48h | 12 credits/s | eligible as narrow fallback |
| Google `veo-3.1-generate-001` | GA | text/image; first/last; reference assets | 4/6/8s; 720/1080/4K; 16:9/9:16 | extension yes; targeted edit not documented | conflicting official docs: probe exact profile | C2PA + SynthID | long-running operation; GCS or bytes | USD/s by resolution/audio | eligible only for probe-confirmed profile |
| AWS `amazon.nova-reel-v1:1` | callable, lifecycle check required | text; optional first-frame image; storyboard | 6s steps to 120s; 1280×720/24fps | no / no | no | Content Credentials + S3 manifests | `StartAsyncInvoke`; caller S3 | live Bedrock price lookup | non-default; reject if lifecycle probe fails |
| OpenAI `sora-2*` | deprecated; shuts 2026-09-24 | text/image | up to 20s; 720p/1080p by model | both | yes | local receipt; no API provenance claim relied on | async poll/webhook; URL 1h | USD/s | migration-only; new plans reject |
| Seedance 2.5 | announced only | unverified | unverified | unverified | unverified | unverified | no official callable API verified | unverified | inactive |

## Required corrections to the existing example record

The current `examples/seedance-provider-capability.json` should not be copied into implementation unchanged:

- replace the marketing identifier `seedance-2.0` with the exact provider model ID `dreamina-seedance-2-0-260128` for the direct BytePlus adapter (or `seedance2` for Runway);
- change `min_duration_seconds` from `1` to `4`;
- do not assert structured `multi_shot: true` without a provider operation and probe demonstrating it;
- add exact output profiles, including full-model-only 4K and Fast/Mini resolution limits;
- add task retention (7 days), output URL retention (24 hours), callback/polling behaviour, and unsupported seed/camera control;
- express the real-human input policy and authorized-asset exception;
- store token-based pricing with its checked timestamp and context-dependent formula;
- distinguish an optional visible watermark from cryptographic provenance;
- keep `active` dependent on an adapter health probe, credentials, provider activation, and a non-expired terms/capability snapshot.

## Implementation decision enabled by this research

Build `video.submit`, `video.poll`, `video.continue`, and `video.edit` against the provider-independent job/receipt contract, not against any one vendor payload. Ship at least one real public-media acquisition adapter and deterministic MP4/WebM composition independently of generative credentials. Then add provider adapters behind feature flags in this order:

1. Runway `seedance2` or direct BytePlus Seedance 2.0, selected by credential/access reality and a conformance probe;
2. Runway Gen-4.5 as a narrow short-plate fallback;
3. Google Veo 3.1 for profiles whose exact audio/resolution capability passes a probe;
4. Nova Reel only when its lifecycle check passes and long storyboarded 720p output is specifically useful.

An unavailable, uncredentialed, exhausted, policy-incompatible, or failed generative provider returns a typed “optional lane unavailable” result to acquisition planning. It does **not** fail Epi-Card release conformance when approved public, imported, or commissioned plates can satisfy the render plan.
