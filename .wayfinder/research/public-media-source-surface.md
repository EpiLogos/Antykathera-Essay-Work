# Production public-media source surface

Research date: 2026-08-01

## Resolution

The Epi-Card v1 runtime should implement a source-neutral procurement contract with five production adapters:

1. **Pexels** — primary general-purpose photo and stock-video source.
2. **Pixabay** — secondary general-purpose image and stock-video source, with stricter caching and acquisition rules.
3. **Wikimedia Commons** — primary open-licence/public-domain source for cultural, historical, scientific, symbolic, and natural image and video material.
4. **NASA Image and Video Library** — domain adapter for NASA-produced space material, especially Apollo, subject to asset-level credit and third-party-rights checks.
5. **Openverse** — broad **image discovery** adapter only. It is an index, not the rights authority or final acquisition authority; every chosen result must be resolved and reverified at its upstream landing page/provider before use.

This surface makes generative video optional rather than foundational. A card can be produced entirely from acquired public images and videos, including locally derived motion from still images.

No reviewed source exposes a production API that returns an arbitrary temporal fragment of a video. Providers return a whole source file or a complete rendition. The Epi-Card runtime must therefore own clip selection (`start_ms`, `end_ms`, rendition choice), download the whole selected rendition to controlled storage, derive the clip locally, and retain hashes and derivation provenance.

## Proposed adapter matrix

| Adapter | Image | Video | Production role | Authentication and current quota | Acquisition and clip surface | Rights and attribution posture |
|---|---:|---:|---|---|---|---|
| Pexels | Yes | Yes | Default broad stock search | API key in `Authorization`; default 200 requests/hour and 20,000/month; quota headers on successful responses | Direct image variants; video renditions expose MIME type, dimensions, FPS and hosted link; full-file acquisition, then local clip | Pexels licence; do not redistribute unaltered/standalone assets; API UI must prominently link to Pexels and should credit creator with source-page link |
| Pixabay | Yes | Yes | Secondary broad stock search | API key in query; default 100 requests/60 seconds; cache API responses 24 hours | Images must be downloaded for permanent use; permanent image hotlinking forbidden; videos may be embedded but local storage is recommended; full-file acquisition, then local clip | Pixabay Content Licence; no standalone distribution; result UI should identify Pixabay; credit is not required by content licence but should be preserved and rendered by Epi-Card |
| Wikimedia Commons | Yes | Yes | Open cultural, historical, scientific and natural material | Public read API; compliant contact-bearing user agent gets 200 requests/minute under the current 2026 tier; respect `Retry-After`, maximum three concurrent requests | Original file plus image derivatives or TimedMediaHandler video derivatives; no temporal fragment endpoint; full rendition then local clip | Per-file licence controls; store creator, credit, licence name/version/URL, attribution requirement and source page; support CC/public-domain obligations asset by asset |
| NASA Image and Video Library | Yes | Yes | NASA/Apollo-specific authoritative media search | Public REST interface; official API documentation states no key requirement or numeric quota; cache and back off on errors | `/search`, `/asset/{nasa_id}`, `/metadata/{nasa_id}`, `/captions/{nasa_id}`; asset collection supplies complete renditions; local clip | NASA material is generally not copyrighted in the US, but third-party material can be embedded and marked; acknowledge NASA, avoid endorsement, and gate identifiable-person/commercial uses |
| Openverse | Yes | **No** (current public API exposes image and audio, not video) | Broad open-image discovery and licence filtering | Anonymous access or OAuth client credentials; published tiers are anonymous/standard/enhanced/exempt, but the current official docs do not publish numeric limits; obey returned rate-limit headers and backoff | Returns direct media URL and upstream landing URL; acquire only after fresh upstream validation | Openverse explicitly does not verify individual licence accuracy or attribution completeness; preserve its generated attribution but verify against the upstream record before approval |

## Provider findings

### Pexels

The [Pexels API documentation](https://www.pexels.com/api/documentation/) exposes photo and video search under a REST JSON API. Authentication is a Pexels API key in the `Authorization` header. The documented default limit is 200 requests per hour and 20,000 requests per month; successful responses carry `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, and `X-Ratelimit-Reset`. Search pagination supports up to 80 records per page.

Photo records include the Pexels page URL, photographer name and profile, dimensions, dominant colour, alternative text, and a family of sized image URLs. Video records include the Pexels landing URL, duration, videographer identity/profile, poster images, and `video_files` renditions with file ID, quality, MIME type, dimensions, FPS, and direct hosted link. Video search filters orientation and minimum size; the popular-video endpoint additionally exposes minimum and maximum duration. There is no in/out-point or clip-download selector.

The content licence and API presentation requirements are distinct and both must be obeyed. The [Pexels licence](https://www.pexels.com/legal-pages/license/) permits free use and modification and says attribution is not required, but prohibits unaltered/standalone resale, false endorsement, offensive treatment of identifiable people, redistribution through stock/wallpaper services, and trademark use. The API documentation separately requires a prominent Pexels link when using API results and asks applications to credit photographers when possible. A conforming adapter should therefore always retain and expose the creator, creator profile, Pexels landing page, provider link, and the acquisition-time licence URL.

Pexels currently does not expose rich semantic metadata: its [official API metadata note](https://help.pexels.com/hc/en-us/articles/47677748516121-Are-media-details-and-statistics-available-through-the-API) says titles, tags, detailed metadata, view counts, download counts, and creator statistics are not available through the API. The runtime must not invent these as provider facts; prompt-derived scene tags remain Epi-Card annotations, separate from source metadata.

**Adapter position:** production default for natural imagery and short stock motion. Acquire chosen renditions promptly; never depend on a remote rendition URL as the durable card asset. Preserve the untouched API response and downloaded-byte hash.

### Pixabay

The [Pixabay API documentation](https://pixabay.com/api/docs/) provides separate image and video search endpoints authenticated by an API key. The default quota is 100 requests per 60 seconds per key, communicated through `X-RateLimit-*` headers. Responses must be cached for 24 hours; systematic mass downloads are prohibited, and the API is intended to serve real user searches.

Image search supports type, orientation, category, size, colour, editor's choice, safesearch, order and pagination. Result records include a source page, contributor identity, tags, image dimensions/size, engagement counts, and multiple image URLs. Original/full-HD image URLs require approved full API access. Medium `webformatURL` values are documented as valid for 24 hours. Permanent image hotlinking is prohibited: selected images must be downloaded to runtime-controlled storage. Video search supports type, category, minimum dimensions, editor's choice, safesearch, ordering and pagination. Records include duration, source page, contributor, tags, and `large`/`medium`/`small`/`tiny` complete MP4 renditions with dimensions, byte size and thumbnail. Videos may be embedded, but Pixabay recommends local storage. Again, no temporal clip endpoint exists.

The [Pixabay Content Licence summary](https://pixabay.com/service/license-summary/) permits free use and adaptation but prohibits standalone distribution, misleading or illegal use, trademark use, and some commercial uses of recognizable brands. It warns that privacy, publicity, trademark and other third-party rights may survive the content licence. The full [Pixabay terms](https://pixabay.com/service/terms/) clarify that a filter, recolouring, resizing or cropping alone remains a standalone use, while a meaningful combination with images, video, text, illustration, background features and editing can constitute a new creative work. The content licence does not require credit, but the API documentation asks the application to show users where search results come from.

**Adapter position:** production fallback and diversity source. Never package the unmodified original as a user-extractable stock file. If the treatment is only a hue/filter/crop, mark the result `rights_review_required`; the normal Epi-Card composition should combine material, text, symbolism, motion and design into the final work. Preserve contributor, profile/source page, licence link, tags, acquisition timestamp, API response and byte hash.

### Wikimedia Commons

Wikimedia Commons covers still images and timed media under per-file licences. Search can use the public [MediaWiki Search API](https://www.mediawiki.org/wiki/API:Search) as a generator in file namespace 6. For still and general file information, [`prop=imageinfo`](https://www.mediawiki.org/wiki/API:Imageinfo) can return original/description URLs, dimensions, byte size, SHA-1, MIME type, media type, metadata, and `extmetadata`. `extmetadata` is expensive and should be requested only for the shortlisted records; it is the relevant source for values such as Artist, Credit, LicenseShortName, LicenseUrl, UsageTerms, AttributionRequired and Copyrighted. HTML-formatted metadata must be sanitized before display but preserved raw in the provenance snapshot.

For audio/video, the [TimedMediaHandler API](https://www.mediawiki.org/wiki/Extension%3ATimedMediaHandler/API) provides `prop=videoinfo` and `viprop=derivatives`; these expose complete transcodes, not arbitrary temporal fragments. Wikimedia's [media reuse guidance](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia/en) permits downloading or linking subject to the licence on the file page, recommends download over hotlinking, and stresses that attribution and share-alike requirements vary by file.

As of the current 2026 [Wikimedia API rate-limit documentation](https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits), an unidentified client is limited to 10 requests/minute; an unauthenticated bot with a compliant contact-bearing User-Agent is limited to 200 requests/minute; established authenticated users receive 2,000/minute. Clients should make no more than three concurrent requests, respect `Retry-After` on 429/503 responses, and back off. The [Wikimedia User-Agent policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy/en) requires a descriptive client/version and contact route rather than a generic library agent.

**Adapter position:** production source for swans, bees, art-historical Apollo imagery, symbols, scientific images and open video. The default automated rights allowlist should initially accept only machine-readable `CC0`, `PDM`, `CC BY` and explicitly reviewed compatible equivalents. `CC BY-SA`, GFDL, noncommercial, no-derivatives, missing or conflicting rights data must route to a licence-policy decision/manual review rather than be silently flattened into “free”.

### NASA Image and Video Library

The official [NASA Image and Video Library API documentation](https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf) defines a public JSON REST root at `https://images-api.nasa.gov` with `/search`, `/asset/{nasa_id}`, `/metadata/{nasa_id}`, `/captions/{nasa_id}`, and `/album/{album_name}`. Search supports fields including free text, description, keywords, location, photographer, NASA ID, media type, paging and year range. Results use Collection+JSON and carry NASA ID, media type, title, description, keywords, creating centre and date; the asset collection resolves available complete renditions, while metadata and captions supply additional records. The document describes ordinary HTTP behaviour and does not require an API key or publish a numeric quota.

The [NASA images and media usage guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/) say NASA content is generally not subject to copyright in the United States and may be used for educational/informational purposes, with NASA acknowledged as source. They also require that use not imply NASA endorsement, warn that some records contain marked third-party copyrighted material, and flag privacy/publicity clearance for commercial use of identifiable people. NASA identifiers and insignia have separate legal restrictions.

**Adapter position:** first-party domain source for Apollo and space imagery, not a blanket “public domain” switch. Store `nasa_id`, all credit/copyright strings, centre, photographer, description, keywords, creation date, landing URL, selected asset URL, media type, captions URL if present, API response and byte hash. Reject or review assets with third-party credit/copyright notices, prominent protected identifiers, or identifiable-person commercial-use concerns.

### Openverse

The current [Openverse API reference](https://api.openverse.org/) exposes image and audio APIs, not a video API. Image search supports source, extension, category, aspect/size, specific licence values, `commercial` and `modification` licence-type filters, sensitive-content filtering, and paging through the top 10,000 relevant results. Returned fields include title, creator/profile, direct media URL, upstream landing URL, upstream source/provider, file data, tags, licence/version/URL, prebuilt attribution, and sensitivity markers. These fields are documented in the official [Openverse media-properties reference](https://docs.openverse.org/meta/media_properties/frontend.html).

Openverse allows anonymous access and OAuth client-credential access. Its [authentication and throttling documentation](https://docs.openverse.org/api/reference/authentication_and_throttling.html) defines anonymous, standard, enhanced and exempt behaviour, but the current public documentation does not publish stable numeric allowances for those tiers. The adapter must read rate-limit headers, implement backoff, and never attempt to circumvent throttling.

Most importantly, the [Openverse Terms of Service](https://docs.openverse.org/terms_of_service.html) state that it aggregates metadata for third-party-hosted works, does not control the content, does not verify licensing status, and requires consumers to observe the source platform's terms. Openverse itself also warns that generated attribution may be inaccurate or incomplete. Therefore an Openverse result is only a discovery candidate. Acquisition approval requires a fresh fetch of the upstream landing record, a working direct asset URL, and verified licence/attribution data. If that cannot be recovered, reject the candidate.

**Adapter position:** broad image discovery, especially where direct stock searches are thin. Preserve both Openverse and upstream identifiers/URLs so provenance is explicitly two-hop.

## Conforming source-neutral contract

Every provider adapter should implement the same four operations:

```text
search(request) -> MediaCandidate[]
resolve(provider_id, foreign_id) -> ResolvedMedia
acquire(resolved_media, rendition_id) -> AcquiredSource
refresh_rights(acquired_source) -> RightsAssessment
```

`MediaCandidate` is for browsing; it must never be renderable as a production asset by itself. `resolve` performs a fresh detail lookup. `acquire` downloads the selected whole rendition into controlled storage and computes its hash. `refresh_rights` checks the live source/rights state before a final export while preserving the acquisition-time evidence rather than overwriting history.

Minimum normalized fields:

```text
provider
provider_media_id
provider_media_url
foreign_source_provider?      # required for aggregators such as Openverse
foreign_source_id?
foreign_landing_url?
media_type                    # image | video
title?
description?
creator_name?
creator_url?
credit_line?
tags[]
provider_metadata_raw
source_created_at?
resolved_at
renditions[]                  # URL, MIME, width, height, bytes?, fps?, duration_ms?
selected_rendition_id
source_downloaded_at
source_sha256
licence_code?
licence_version?
licence_url?
rights_statement_raw?
rights_source_url
rights_checked_at
attribution_required
attribution_text
commercial_use               # allowed | disallowed | unknown
derivatives                  # allowed | disallowed | unknown
share_alike                   # yes | no | unknown
standalone_distribution      # allowed | disallowed | unknown
personality_trademark_risk   # clear | review | reject
sensitivity_flags[]
rights_status                 # approved | review_required | rejected
```

Provider metadata and Epi-Card interpretation must remain separate. A scene's symbolic terms, QL positions, Pasu-derived allusions and generated descriptions are card-authored annotations; they are not to be written into the source's title, tags, creator fields or licence evidence.

## Clip-selection and derivation contract

Because each source supplies whole files, the common video selector should be owned by the runtime:

```text
source_sha256
rendition_id
start_ms
end_ms
source_duration_ms
transform_recipe_version
ffmpeg_arguments
derived_sha256
derived_duration_ms
derived_width
derived_height
derived_fps
audio_policy                  # preserve | mute | replace
```

Validate `0 <= start_ms < end_ms <= source_duration_ms`. Do not accept a “clip” that depends on a remote query fragment. Download, probe and hash the complete rendition first; derive the requested segment deterministically; then probe and hash the derived clip. Keep both the source record and derivation record even if the distributable `.epicard` contains only the transformed/rendered result.

## Production gates

1. **No rights-blind fallback.** Search success does not imply acquisition approval.
2. **No remote-only production asset.** A selected source is copied to controlled storage, probed and hashed before rendering.
3. **No unmodified source export.** The distributable package contains the rendered Epi-Card and attribution/provenance ledger, not user-extractable stock originals, unless a specific asset licence and package policy explicitly permit it.
4. **No thin-transform assumption.** Hue, filter, resize or crop alone is insufficient for Pixabay's non-standalone requirement and should trigger review. The normal card treatment should make a genuine composed work.
5. **Attribution is render-target aware.** Web, video, card-detail, print and package-manifest outputs all need a way to carry required credit and licence links/text.
6. **Rights are evidence, not a boolean.** Preserve the provider response, source page/landing URL, terms/licence URL, lookup timestamps, selected rendition, source hash and final derivation chain.
7. **Recheck before export.** A removed asset, changed licence, broken upstream record or conflicting rights statement prevents an unattended final export and routes to review.
8. **Provider loss is non-fatal.** The procurement layer ranks candidates across adapters and can complete a card without Seedance or any single public-media provider.

## Decision for the runtime map

The public-media procurement contract can now be specified around this adapter surface. The immediate implementation decision is not “Seedance or public media”; it is a multi-route resolver in which public acquisition is a first-class production path and generative video is an optional provider class. The runtime should ship with at least Pexels, Pixabay, Wikimedia Commons and NASA active, plus Openverse image discovery with mandatory upstream verification.
