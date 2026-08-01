-- Epi-Card QL Conjugate System v1.0.0
-- Canonical production schema for PostgreSQL 18+
-- PostgreSQL 18 is required because the schema uses core uuidv7().
-- All timestamps are UTC timestamptz. Human-local time and timezone are stored explicitly.

BEGIN;

CREATE SCHEMA IF NOT EXISTS epicard;
SET search_path = epicard, public;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE disclosure_class AS ENUM ('secret', 'private', 'shared', 'public');
CREATE TYPE actor_kind AS ENUM ('human', 'agent', 'service', 'provider');
CREATE TYPE pasu_kind AS ENUM ('human', 'collective', 'anonymous', 'other');
CREATE TYPE engagement_status AS ENUM (
  'draft', 'mapping', 'art_direction', 'production', 'review',
  'approved', 'rendered', 'published', 'returned', 'archived'
);
CREATE TYPE ql_phase AS ENUM ('bimba', 'pratibimba');
CREATE TYPE ql_occupancy AS ENUM (
  'present', 'latent', 'missing', 'unknown', 'withheld', 'conflicted', 'overdetermined'
);
CREATE TYPE ql_assignment_role AS ENUM (
  'direct', 'distributed', 'condensed', 'supporting', 'counterposed', 'unassigned'
);
CREATE TYPE evidence_register AS ENUM (
  'exact_identity', 'ql_derived', 'canonical_symbolic',
  'cross_register', 'archetypal_reception', 'open_extension'
);
CREATE TYPE action_side_effect AS ENUM ('read', 'write', 'generate', 'render', 'publish');
CREATE TYPE action_gate_mode AS ENUM ('none', 'conditional', 'required');
CREATE TYPE action_gate_stage AS ENUM ('pre_execute', 'pre_commit', 'pre_promote', 'pre_publish');
CREATE TYPE action_gate_kind AS ENUM ('provider_disclosure', 'consent', 'human_review', 'human_approval', 'actor_authorization', 'account_authorization', 'prior_approval');
CREATE TYPE action_gate_decision AS ENUM ('not_applicable', 'passed', 'blocked');
CREATE TYPE action_run_status AS ENUM (
  'queued', 'running', 'awaiting_external', 'awaiting_review',
  'succeeded', 'failed_retryable', 'failed_terminal', 'cancelled'
);
CREATE TYPE approval_status AS ENUM ('requested', 'approved', 'rejected', 'revoked');
CREATE TYPE asset_role AS ENUM (
  'source', 'reference', 'candidate', 'canonical', 'intermediate', 'rendition',
  'poster', 'mask', 'symbol', 'font_outline', 'audio_layer', 'transcript',
  'storyboard', 'print', 'knowledge_export', 'validation_report'
);
CREATE TYPE alpha_mode AS ENUM ('none', 'straight', 'premultiplied');
CREATE TYPE basin_relation AS ENUM (
  'essential', 'constitutive', 'contextual', 'resonant',
  'counterpole', 'boundary', 'excluded', 'unresolved'
);
CREATE TYPE relation_direction AS ENUM ('directed', 'undirected');
CREATE TYPE symbol_resolution_mode AS ENUM ('reuse', 'parameterise', 'transform', 'combine', 'generate_new');
CREATE TYPE scene_reciprocity_mode AS ENUM (
  'phase_flip', 'crossfade', 'interleaved', 'split_field',
  'masked_reveal', 'conjugate_cut', 'audio_visual_exchange'
);
CREATE TYPE validation_severity AS ENUM ('info', 'warning', 'error', 'fatal');
CREATE TYPE publication_status AS ENUM (
  'prepared', 'awaiting_approval', 'approved', 'submitting',
  'processing', 'published', 'failed_retryable', 'failed_terminal', 'revoked'
);

CREATE TABLE schema_revision (
  version             text PRIMARY KEY,
  applied_at          timestamptz NOT NULL DEFAULT now(),
  specification_hash  char(64) NOT NULL,
  notes               text
);

CREATE TABLE actor (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  kind                 actor_kind NOT NULL,
  display_name         text,
  external_ref         text,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  metadata             jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at           timestamptz NOT NULL DEFAULT now(),
  updated_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (kind, external_ref)
);

CREATE TABLE pasu (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  kind                 pasu_kind NOT NULL,
  public_handle        text,
  private_profile_ref  text,
  locale               text,
  timezone_default     text,
  consent_profile      jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  updated_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE pasu_attribute (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  pasu_id              uuid NOT NULL REFERENCES pasu(id) ON DELETE CASCADE,
  attribute_type       text NOT NULL,
  value                jsonb NOT NULL,
  source_ref           text,
  valid_from           timestamptz,
  valid_to             timestamptz,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  external_provider_ok boolean NOT NULL DEFAULT false,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to > valid_from)
);
CREATE INDEX pasu_attribute_lookup_idx ON pasu_attribute (pasu_id, attribute_type);

CREATE TABLE pasu_snapshot (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  pasu_id              uuid NOT NULL REFERENCES pasu(id),
  snapshot             jsonb NOT NULL,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  source_attribute_ids uuid[] NOT NULL DEFAULT '{}',
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE epi_session (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  pasu_id              uuid REFERENCES pasu(id),
  parent_session_id    uuid REFERENCES epi_session(id),
  continuation_of_id   uuid REFERENCES epi_session(id),
  session_key_hash     bytea NOT NULL UNIQUE,
  harness              text,
  harness_session_ref  text,
  started_at           timestamptz NOT NULL DEFAULT now(),
  ended_at             timestamptz,
  timezone             text NOT NULL,
  locale               text,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  resumable_state      jsonb NOT NULL DEFAULT '{}'::jsonb,
  last_event_sequence  bigint NOT NULL DEFAULT 0,
  created_by           uuid REFERENCES actor(id),
  CHECK (ended_at IS NULL OR ended_at >= started_at)
);
CREATE INDEX epi_session_harness_idx ON epi_session (harness, harness_session_ref);

CREATE TABLE temporal_snapshot (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  session_id           uuid NOT NULL REFERENCES epi_session(id),
  event_time           timestamptz,
  observed_at          timestamptz NOT NULL,
  local_civil_time     timestamp,
  timezone             text NOT NULL,
  location             jsonb,
  location_precision   text,
  astronomy_provider   text,
  astronomy_version    text,
  astrology_profile_id text,
  astrology_profile_version text,
  astronomical_facts   jsonb NOT NULL DEFAULT '{}'::jsonb,
  interpreted_contributions jsonb NOT NULL DEFAULT '{}'::jsonb,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE configuration_profile (
  id                   text NOT NULL,
  version              text NOT NULL,
  profile_type         text NOT NULL CHECK (profile_type IN (
    'ql_lens', 'ql_relation', 'mapping', 'disclosure', 'validation',
    'duration', 'render', 'print', 'interaction', 'symbol_baseline',
    'audio_tuning', 'audio_resonator', 'spatial', 'provider_policy', 'other'
  )),
  status               text NOT NULL CHECK (status IN ('draft', 'active', 'deprecated', 'retired')),
  register             evidence_register NOT NULL DEFAULT 'ql_derived',
  content              jsonb NOT NULL,
  content_hash         char(64) NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'),
  source_refs          jsonb NOT NULL DEFAULT '[]'::jsonb,
  change_log           jsonb NOT NULL DEFAULT '[]'::jsonb,
  author_actor_id      uuid REFERENCES actor(id),
  reviewer_actor_ids   uuid[] NOT NULL DEFAULT '{}',
  effective_from       timestamptz,
  effective_to         timestamptz,
  created_at           timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (id, version),
  CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to > effective_from)
);

CREATE TABLE profile_set (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  stable_key           text NOT NULL,
  version              text NOT NULL,
  status               text NOT NULL CHECK (status IN ('draft', 'active', 'deprecated', 'retired')),
  set_hash             char(64) NOT NULL CHECK (set_hash ~ '^[0-9a-f]{64}$'),
  description          text,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (stable_key, version),
  UNIQUE (set_hash)
);

CREATE TABLE profile_set_member (
  profile_set_id       uuid NOT NULL REFERENCES profile_set(id) ON DELETE CASCADE,
  registry             text NOT NULL CHECK (registry IN (
    'configuration', 'correspondence', 'projection', 'provider_capability'
  )),
  profile_id           text NOT NULL,
  profile_version      text NOT NULL,
  precedence           integer NOT NULL DEFAULT 0,
  required             boolean NOT NULL DEFAULT true,
  PRIMARY KEY (profile_set_id, registry, profile_id, profile_version)
);

CREATE TABLE attractor (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  kind                 text NOT NULL,
  stable_key           text UNIQUE,
  label                text NOT NULL,
  description          text,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  updated_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE attractor_revision (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  attractor_id         uuid NOT NULL REFERENCES attractor(id) ON DELETE CASCADE,
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  label                text NOT NULL,
  description          text,
  metadata             jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (attractor_id, revision_no)
);

CREATE TABLE basin_member (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  attractor_revision_id uuid NOT NULL REFERENCES attractor_revision(id) ON DELETE CASCADE,
  stable_local_key     text NOT NULL,
  label                text NOT NULL,
  description          text,
  relation             basin_relation NOT NULL,
  weight               numeric(6,5) NOT NULL CHECK (weight >= 0 AND weight <= 1),
  register             evidence_register NOT NULL,
  rationale            text NOT NULL,
  ql_candidate_addresses text[] NOT NULL DEFAULT '{}',
  valid_from           timestamptz,
  valid_to             timestamptz,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (attractor_revision_id, stable_local_key, relation),
  CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to > valid_from)
);
CREATE INDEX basin_member_relation_idx ON basin_member (attractor_revision_id, relation);

CREATE TABLE engagement (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  slug                 text UNIQUE,
  pasu_snapshot_id     uuid REFERENCES pasu_snapshot(id),
  temporal_snapshot_id uuid REFERENCES temporal_snapshot(id),
  attractor_revision_id uuid NOT NULL REFERENCES attractor_revision(id),
  question             text,
  intention            text,
  active_lens_id       text NOT NULL,
  active_lens_version  text NOT NULL,
  profile_set          jsonb NOT NULL DEFAULT '{}'::jsonb,
  profile_set_id       uuid REFERENCES profile_set(id),
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  status               engagement_status NOT NULL DEFAULT 'draft',
  current_revision     integer NOT NULL DEFAULT 1 CHECK (current_revision > 0),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  updated_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE engagement_projection (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  projection_kind      text NOT NULL CHECK (projection_kind IN ('private', 'shared', 'public', 'provider')),
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  disclosure           disclosure_class NOT NULL,
  provider             text,
  purpose              text,
  source_revision_manifest jsonb NOT NULL,
  snapshot             jsonb NOT NULL,
  snapshot_hash        char(64) NOT NULL CHECK (snapshot_hash ~ '^[0-9a-f]{64}$'),
  status               text NOT NULL CHECK (status IN ('draft', 'approved', 'superseded', 'expired')),
  expires_at           timestamptz,
  created_by           uuid REFERENCES actor(id),
  approved_by          uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  approved_at          timestamptz,
  UNIQUE (engagement_id, projection_kind, provider, purpose, revision_no),
  UNIQUE (snapshot_hash),
  CHECK ((projection_kind='provider' AND provider IS NOT NULL AND purpose IS NOT NULL)
      OR (projection_kind<>'provider'))
);
CREATE INDEX engagement_projection_lookup_idx
  ON engagement_projection (engagement_id, projection_kind, status, revision_no DESC);

CREATE TABLE resource_lock (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  target_kind          text NOT NULL,
  target_id            uuid NOT NULL,
  field_path           text NOT NULL DEFAULT '',
  lock_type            text NOT NULL CHECK (lock_type IN (
    'semantic', 'symbol_geometry', 'palette_token', 'typography',
    'scene_intent', 'plate', 'audio_tuning', 'render', 'publication'
  )),
  reason               text NOT NULL,
  locked_by            uuid NOT NULL REFERENCES actor(id),
  locked_at            timestamptz NOT NULL DEFAULT now(),
  expires_at           timestamptz,
  released_by          uuid REFERENCES actor(id),
  released_at          timestamptz,
  release_reason       text,
  CHECK (released_at IS NULL OR released_at >= locked_at),
  CHECK (expires_at IS NULL OR expires_at > locked_at)
);
CREATE UNIQUE INDEX resource_lock_active_unique_idx
  ON resource_lock (engagement_id, target_kind, target_id, field_path)
  WHERE released_at IS NULL;

CREATE TABLE engagement_session (
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  session_id           uuid NOT NULL REFERENCES epi_session(id) ON DELETE CASCADE,
  role                 text NOT NULL CHECK (role IN ('originating', 'continuing', 'reviewing', 'publishing')),
  joined_at            timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (engagement_id, session_id, role)
);

CREATE TABLE talismanic_activation (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL UNIQUE REFERENCES engagement(id) ON DELETE CASCADE,
  intent_statement     text NOT NULL,
  recipient_pasu_id    uuid REFERENCES pasu(id),
  activation_scope     text,
  activation_at        timestamptz,
  activation_event     text,
  review_at            timestamptz,
  expiry_condition     text,
  return_condition     text,
  handling_notes       text,
  private_phrase_ref   text,
  cadence_or_repetition jsonb,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE activation_witness (
  activation_id        uuid NOT NULL REFERENCES talismanic_activation(id) ON DELETE CASCADE,
  actor_id             uuid NOT NULL REFERENCES actor(id),
  role                 text NOT NULL DEFAULT 'witness',
  PRIMARY KEY (activation_id, actor_id, role)
);

CREATE TABLE source_form (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  source_kind          text NOT NULL,
  declared_arity       integer CHECK (declared_arity >= 0),
  native_relations     jsonb NOT NULL DEFAULT '[]'::jsonb,
  source_ref           text,
  notes                text,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE source_member (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  source_form_id       uuid NOT NULL REFERENCES source_form(id) ON DELETE CASCADE,
  ordinal              integer,
  member_key           text,
  content              jsonb NOT NULL,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE NULLS NOT DISTINCT (source_form_id, ordinal),
  UNIQUE NULLS NOT DISTINCT (source_form_id, member_key)
);

CREATE TABLE asset (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  sha256               char(64) NOT NULL UNIQUE CHECK (sha256 ~ '^[0-9a-f]{64}$'),
  uri                  text NOT NULL,
  media_type           text NOT NULL,
  role                 asset_role NOT NULL,
  byte_length          bigint CHECK (byte_length IS NULL OR byte_length >= 0),
  width                integer CHECK (width IS NULL OR width > 0),
  height               integer CHECK (height IS NULL OR height > 0),
  duration_ms          bigint CHECK (duration_ms IS NULL OR duration_ms >= 0),
  alpha_mode           alpha_mode NOT NULL DEFAULT 'none',
  colour_profile       text,
  sample_rate          integer CHECK (sample_rate IS NULL OR sample_rate > 0),
  bit_depth            integer CHECK (bit_depth IS NULL OR bit_depth > 0),
  rights_status        text NOT NULL DEFAULT 'unknown',
  licence              text,
  creator_actor_id     uuid REFERENCES actor(id),
  provider             text,
  model_id             text,
  model_version        text,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  metadata             jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at           timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX asset_role_idx ON asset (role);
CREATE INDEX asset_provider_idx ON asset (provider, model_id, model_version);

CREATE TABLE asset_derivation (
  output_asset_id      uuid NOT NULL REFERENCES asset(id) ON DELETE CASCADE,
  input_asset_id       uuid NOT NULL REFERENCES asset(id),
  relation             text NOT NULL CHECK (relation IN ('derived_from', 'references', 'contains', 'mask_of', 'mixes', 'continues')),
  operation_name       text,
  operation_version    text,
  parameters           jsonb NOT NULL DEFAULT '{}'::jsonb,
  sequence_no          integer NOT NULL DEFAULT 0,
  PRIMARY KEY (output_asset_id, input_asset_id, relation, sequence_no),
  CHECK (output_asset_id <> input_asset_id)
);

CREATE TABLE recording (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  session_id           uuid NOT NULL REFERENCES epi_session(id),
  engagement_id        uuid REFERENCES engagement(id),
  asset_id             uuid NOT NULL REFERENCES asset(id),
  recorded_at          timestamptz,
  speaker_map          jsonb NOT NULL DEFAULT '{}'::jsonb,
  consent_state        text NOT NULL,
  language_hints       text[] NOT NULL DEFAULT '{}',
  capture_metadata     jsonb NOT NULL DEFAULT '{}'::jsonb,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE transcript (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  recording_id         uuid NOT NULL REFERENCES recording(id) ON DELETE CASCADE,
  provider             text NOT NULL,
  model_id             text NOT NULL,
  model_version        text,
  language             text,
  diarisation_map      jsonb NOT NULL DEFAULT '{}'::jsonb,
  transcript_asset_id  uuid REFERENCES asset(id),
  digest               char(64) CHECK (digest IS NULL OR digest ~ '^[0-9a-f]{64}$'),
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE transcript_segment (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  transcript_id        uuid NOT NULL REFERENCES transcript(id) ON DELETE CASCADE,
  ordinal              integer NOT NULL CHECK (ordinal >= 0),
  speaker_ref          text,
  start_ms             bigint NOT NULL CHECK (start_ms >= 0),
  end_ms               bigint NOT NULL CHECK (end_ms > start_ms),
  text                 text NOT NULL,
  confidence           numeric(6,5) CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
  redacted             boolean NOT NULL DEFAULT false,
  disclosure           disclosure_class NOT NULL DEFAULT 'private',
  UNIQUE (transcript_id, ordinal)
);

CREATE TABLE ql_frame_revision (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  prior_revision_id    uuid REFERENCES ql_frame_revision(id),
  threshold_snapshot   jsonb NOT NULL,
  frame_snapshot       jsonb NOT NULL,
  frame_hash           char(64) NOT NULL CHECK (frame_hash ~ '^[0-9a-f]{64}$'),
  status               text NOT NULL CHECK (status IN ('proposed', 'approved', 'superseded')),
  created_by           uuid REFERENCES actor(id),
  approved_by          uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  approved_at          timestamptz,
  UNIQUE (engagement_id, revision_no),
  UNIQUE (engagement_id, frame_hash),
  CHECK (prior_revision_id IS NULL OR prior_revision_id <> id),
  CHECK (status <> 'approved' OR approved_at IS NOT NULL)
);

ALTER TABLE engagement
  ADD COLUMN current_ql_frame_revision_id uuid REFERENCES ql_frame_revision(id);

CREATE TABLE ql_position (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  phase                ql_phase NOT NULL,
  position_index       smallint NOT NULL CHECK (position_index BETWEEN 0 AND 5),
  address              text GENERATED ALWAYS AS (
    CASE phase
      WHEN 'bimba' THEN 'P' || position_index::text
      ELSE 'P' || position_index::text || '′'
    END
  ) STORED,
  canonical_unit       text NOT NULL,
  canonical_question   text NOT NULL,
  structural_role      text NOT NULL,
  local_label          text,
  local_question       text,
  short_summary        text,
  extended_articulation text,
  occupancy            ql_occupancy NOT NULL DEFAULT 'unknown',
  occupancy_reason     text,
  salience             numeric(6,5) NOT NULL DEFAULT 0.5 CHECK (salience >= 0 AND salience <= 1),
  revision_no          integer NOT NULL DEFAULT 1 CHECK (revision_no > 0),
  approved_at          timestamptz,
  approved_by          uuid REFERENCES actor(id),
  UNIQUE (engagement_id, phase, position_index),
  UNIQUE (engagement_id, address),
  CHECK (occupancy NOT IN ('missing', 'withheld', 'unknown') OR occupancy_reason IS NOT NULL)
);
CREATE INDEX ql_position_engagement_order_idx ON ql_position (engagement_id, phase, position_index);

CREATE TABLE ql_relation (
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  source_position_id   uuid NOT NULL REFERENCES ql_position(id) ON DELETE CASCADE,
  target_position_id   uuid NOT NULL REFERENCES ql_position(id) ON DELETE CASCADE,
  relation_type        text NOT NULL CHECK (relation_type IN (
    'adjacent', 'klein_twist', 'enriched_return', 'conjugate',
    'complement', 'explicate_partition', 'implicate_partition',
    'physical_triad', 'contextual_triad'
  )),
  direction            relation_direction NOT NULL,
  sequence_no          integer,
  metadata             jsonb NOT NULL DEFAULT '{}'::jsonb,
  PRIMARY KEY (engagement_id, source_position_id, target_position_id, relation_type),
  CHECK (source_position_id <> target_position_id)
);

CREATE TABLE ql_assignment (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  ql_position_id       uuid REFERENCES ql_position(id) ON DELETE CASCADE,
  source_member_id     uuid NOT NULL REFERENCES source_member(id) ON DELETE CASCADE,
  role                 ql_assignment_role NOT NULL,
  weight               numeric(6,5) NOT NULL CHECK (weight >= 0 AND weight <= 1),
  register             evidence_register NOT NULL,
  rationale            text NOT NULL,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  CHECK ((role='unassigned' AND ql_position_id IS NULL) OR (role<>'unassigned' AND ql_position_id IS NOT NULL)),
  UNIQUE NULLS NOT DISTINCT (ql_position_id, source_member_id, role)
);

CREATE TABLE claim (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  ql_position_id       uuid REFERENCES ql_position(id) ON DELETE CASCADE,
  claim_text           text NOT NULL,
  register             evidence_register NOT NULL,
  confidence           numeric(6,5) CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
  status               text NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed', 'accepted', 'rejected', 'superseded')),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE evidence_link (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  target_kind          text NOT NULL CHECK (target_kind IN (
    'basin_member', 'claim', 'ql_assignment', 'resonance_contribution',
    'symbol_revision', 'scene_atom', 'audio_state', 'audit_position', 'return_deposit'
  )),
  target_id            uuid NOT NULL,
  source_kind          text NOT NULL CHECK (source_kind IN (
    'source_member', 'asset', 'transcript_segment', 'temporal_snapshot',
    'pasu_attribute', 'prior_engagement', 'external_reference'
  )),
  source_id            uuid,
  source_uri           text,
  selector             jsonb NOT NULL DEFAULT '{}'::jsonb,
  relation             text NOT NULL,
  register             evidence_register NOT NULL,
  note                 text,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  CHECK ((source_id IS NOT NULL) OR (source_uri IS NOT NULL))
);
CREATE INDEX evidence_target_idx ON evidence_link (target_kind, target_id);
CREATE INDEX evidence_source_idx ON evidence_link (source_kind, source_id);

CREATE TABLE return_deposit (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL UNIQUE REFERENCES engagement(id) ON DELETE CASCADE,
  self_implication     text NOT NULL,
  remainder            text NOT NULL,
  achieved_work        text,
  external_implications jsonb NOT NULL DEFAULT '[]'::jsonb,
  next_ground          text NOT NULL,
  next_seed_set        jsonb NOT NULL DEFAULT '[]'::jsonb,
  semantic_delta       jsonb NOT NULL DEFAULT '{}'::jsonb,
  media_delta          jsonb NOT NULL DEFAULT '{}'::jsonb,
  next_engagement_id   uuid REFERENCES engagement(id),
  loop_profile_id      text,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  CHECK (next_engagement_id IS NULL OR next_engagement_id <> engagement_id)
);

CREATE TABLE correspondence_profile (
  id                   text NOT NULL,
  version              text NOT NULL,
  status               text NOT NULL CHECK (status IN ('draft', 'active', 'deprecated', 'retired')),
  scope                text NOT NULL,
  register             evidence_register NOT NULL,
  author_actor_id      uuid REFERENCES actor(id),
  rules                jsonb NOT NULL,
  change_log           jsonb NOT NULL DEFAULT '[]'::jsonb,
  effective_from       timestamptz,
  effective_to         timestamptz,
  created_at           timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (id, version),
  CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to > effective_from)
);

CREATE TABLE resonance_contribution (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  ql_position_id       uuid REFERENCES ql_position(id) ON DELETE CASCADE,
  source_system        text NOT NULL,
  source_selector      text NOT NULL,
  source_value         jsonb NOT NULL,
  phase                double precision CHECK (phase IS NULL OR (phase >= 0 AND phase < 1)),
  register_log2        double precision,
  pulse                double precision CHECK (pulse IS NULL OR pulse >= 0),
  amplitude            double precision CHECK (amplitude IS NULL OR (amplitude >= 0 AND amplitude <= 1)),
  coherence            double precision CHECK (coherence IS NULL OR (coherence >= 0 AND coherence <= 1)),
  bandwidth            double precision CHECK (bandwidth IS NULL OR (bandwidth >= 0 AND bandwidth <= 1)),
  polarity             double precision CHECK (polarity IS NULL OR (polarity >= -1 AND polarity <= 1)),
  ratio_set            jsonb NOT NULL DEFAULT '[]'::jsonb,
  elemental_vector     jsonb NOT NULL DEFAULT '{}'::jsonb,
  chakra_vector        jsonb NOT NULL DEFAULT '{}'::jsonb,
  weight               double precision NOT NULL CHECK (weight >= 0 AND weight <= 1),
  register             evidence_register NOT NULL,
  rationale            text NOT NULL,
  profile_id           text NOT NULL,
  profile_version      text NOT NULL,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (profile_id, profile_version) REFERENCES correspondence_profile(id, version)
);

CREATE TABLE resonance_state (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  ql_position_id       uuid REFERENCES ql_position(id) ON DELETE CASCADE,
  phase                double precision NOT NULL CHECK (phase >= 0 AND phase < 1),
  register_log2        double precision NOT NULL,
  pulse                double precision NOT NULL CHECK (pulse >= 0),
  amplitude            double precision NOT NULL CHECK (amplitude >= 0 AND amplitude <= 1),
  coherence            double precision NOT NULL CHECK (coherence >= 0 AND coherence <= 1),
  bandwidth            double precision NOT NULL CHECK (bandwidth >= 0 AND bandwidth <= 1),
  polarity             double precision NOT NULL CHECK (polarity >= -1 AND polarity <= 1),
  ratio_set            jsonb NOT NULL,
  elemental_vector     jsonb NOT NULL,
  chakra_vector        jsonb NOT NULL,
  profile_set_hash     char(64) NOT NULL CHECK (profile_set_hash ~ '^[0-9a-f]{64}$'),
  calculation_receipt  jsonb NOT NULL,
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE NULLS NOT DISTINCT (engagement_id, ql_position_id, profile_set_hash)
);

CREATE TABLE projection_profile (
  id                   text NOT NULL,
  version              text NOT NULL,
  modality             text NOT NULL CHECK (modality IN ('audio', 'colour', 'geometry', 'typography', 'motion', 'editing_pace', 'light_material', 'spatial')),
  parameters           jsonb NOT NULL,
  transforms           jsonb NOT NULL,
  clamps               jsonb NOT NULL DEFAULT '{}'::jsonb,
  defaults             jsonb NOT NULL DEFAULT '{}'::jsonb,
  inverse_labels       jsonb NOT NULL DEFAULT '{}'::jsonb,
  status               text NOT NULL CHECK (status IN ('draft', 'active', 'deprecated', 'retired')),
  created_at           timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (id, version)
);

CREATE TABLE projected_parameter_set (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  resonance_state_id   uuid NOT NULL REFERENCES resonance_state(id) ON DELETE CASCADE,
  projection_profile_id text NOT NULL,
  projection_profile_version text NOT NULL,
  modality             text NOT NULL,
  parameters           jsonb NOT NULL,
  calculation_receipt  jsonb NOT NULL,
  created_at           timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (projection_profile_id, projection_profile_version)
    REFERENCES projection_profile(id, version),
  UNIQUE (resonance_state_id, projection_profile_id, projection_profile_version)
);

CREATE TABLE art_direction_revision (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  palette_tokens       jsonb NOT NULL,
  typography_signature jsonb NOT NULL,
  geometry_direction   jsonb NOT NULL,
  motion_direction     jsonb NOT NULL,
  light_material_direction jsonb NOT NULL,
  constraints          jsonb NOT NULL DEFAULT '{}'::jsonb,
  locked_paths         text[] NOT NULL DEFAULT '{}',
  status               text NOT NULL CHECK (status IN ('draft', 'proposed', 'approved', 'superseded')),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (engagement_id, revision_no)
);

CREATE TABLE symbol_family (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  stable_key           text UNIQUE,
  name                 text NOT NULL,
  semantic_operation   text NOT NULL,
  invariant_grammar    jsonb NOT NULL,
  resonance_signature  jsonb NOT NULL DEFAULT '{}'::jsonb,
  primary_svg_asset_id uuid REFERENCES asset(id),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  updated_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE symbol_relation (
  source_symbol_id     uuid NOT NULL REFERENCES symbol_family(id) ON DELETE CASCADE,
  target_symbol_id     uuid NOT NULL REFERENCES symbol_family(id) ON DELETE CASCADE,
  relation             text NOT NULL CHECK (relation IN (
    'conjugate', 'inverse', 'contains', 'variant',
    'shares_operation', 'shares_topology', 'returns_to'
  )),
  weight               numeric(6,5) CHECK (weight IS NULL OR (weight >= 0 AND weight <= 1)),
  rationale            text,
  PRIMARY KEY (source_symbol_id, target_symbol_id, relation),
  CHECK (source_symbol_id <> target_symbol_id)
);

CREATE TABLE symbol_revision (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  symbol_family_id     uuid NOT NULL REFERENCES symbol_family(id) ON DELETE CASCADE,
  engagement_id        uuid REFERENCES engagement(id),
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  resolution_mode      symbol_resolution_mode NOT NULL,
  grammar              jsonb NOT NULL,
  canonical_svg_asset_id uuid REFERENCES asset(id),
  monochrome_svg_asset_id uuid REFERENCES asset(id),
  status               text NOT NULL CHECK (status IN ('candidate', 'validated', 'approved', 'superseded')),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (symbol_family_id, revision_no)
);

CREATE TABLE symbol_state (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  symbol_revision_id   uuid NOT NULL REFERENCES symbol_revision(id) ON DELETE CASCADE,
  ql_position_id       uuid NOT NULL REFERENCES ql_position(id) ON DELETE CASCADE,
  transformation       jsonb NOT NULL,
  svg_asset_id         uuid REFERENCES asset(id),
  alpha_asset_id       uuid REFERENCES asset(id),
  mask_asset_id        uuid REFERENCES asset(id),
  loop_anchor          jsonb NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (symbol_revision_id, ql_position_id)
);

CREATE TABLE storyboard_revision (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  profile              text NOT NULL CHECK (profile IN ('base', 'extended', 'custom')),
  width                integer NOT NULL CHECK (width > 0),
  height               integer NOT NULL CHECK (height > 0),
  fps_num              integer NOT NULL CHECK (fps_num > 0),
  fps_den              integer NOT NULL DEFAULT 1 CHECK (fps_den > 0),
  duration_frames      integer NOT NULL CHECK (duration_frames > 0),
  storyboard_asset_id  uuid REFERENCES asset(id),
  status               text NOT NULL CHECK (status IN ('draft', 'approved', 'superseded')),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (engagement_id, revision_no)
);

CREATE TABLE scene_pair (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  storyboard_revision_id uuid NOT NULL REFERENCES storyboard_revision(id) ON DELETE CASCADE,
  position_index       smallint NOT NULL CHECK (position_index BETWEEN 0 AND 5),
  order_index          smallint NOT NULL CHECK (order_index BETWEEN 0 AND 5),
  start_frame          integer NOT NULL CHECK (start_frame >= 0),
  duration_frames      integer NOT NULL CHECK (duration_frames > 0),
  reciprocity_mode     scene_reciprocity_mode NOT NULL,
  transition_in        jsonb NOT NULL DEFAULT '{}'::jsonb,
  transition_out       jsonb NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (storyboard_revision_id, position_index),
  UNIQUE (storyboard_revision_id, order_index)
);

CREATE TABLE scene_atom (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  scene_pair_id        uuid NOT NULL REFERENCES scene_pair(id) ON DELETE CASCADE,
  ql_position_id       uuid NOT NULL REFERENCES ql_position(id) ON DELETE CASCADE,
  face_order           smallint NOT NULL CHECK (face_order IN (0, 1)),
  intent               jsonb NOT NULL,
  visual_action        text NOT NULL,
  camera               jsonb NOT NULL DEFAULT '{}'::jsonb,
  light_material       jsonb NOT NULL DEFAULT '{}'::jsonb,
  generation_plan      jsonb NOT NULL,
  accepted_plate_asset_id uuid REFERENCES asset(id),
  occupancy            ql_occupancy NOT NULL DEFAULT 'unknown',
  UNIQUE (scene_pair_id, ql_position_id),
  UNIQUE (scene_pair_id, face_order)
);

CREATE TABLE provider_capability (
  provider             text NOT NULL,
  model_id             text NOT NULL,
  model_version        text NOT NULL,
  capability_version   text NOT NULL,
  modalities_in        text[] NOT NULL,
  modalities_out       text[] NOT NULL,
  limits               jsonb NOT NULL,
  features             jsonb NOT NULL,
  constraints          jsonb NOT NULL DEFAULT '{}'::jsonb,
  terms_snapshot_ref   text,
  active               boolean NOT NULL DEFAULT true,
  checked_at           timestamptz NOT NULL,
  PRIMARY KEY (provider, model_id, model_version, capability_version)
);

CREATE TABLE provider_job (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  provider             text NOT NULL,
  model_id             text NOT NULL,
  model_version        text NOT NULL,
  provider_job_id      text,
  operation            text NOT NULL,
  request_payload      jsonb NOT NULL,
  request_hash         char(64) NOT NULL CHECK (request_hash ~ '^[0-9a-f]{64}$'),
  status               text NOT NULL,
  resume_cursor        jsonb,
  response_payload     jsonb,
  submitted_at         timestamptz,
  completed_at         timestamptz,
  UNIQUE (provider, provider_job_id)
);

CREATE TABLE audio_palette_revision (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  reference_hz         double precision NOT NULL CHECK (reference_hz > 0),
  ratio_set            jsonb NOT NULL,
  tuning_profile       jsonb NOT NULL,
  resonator_profile    jsonb NOT NULL,
  spatial_profile      jsonb NOT NULL,
  status               text NOT NULL CHECK (status IN ('draft', 'approved', 'superseded')),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (engagement_id, revision_no)
);

CREATE TABLE audio_state (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  audio_palette_revision_id uuid NOT NULL REFERENCES audio_palette_revision(id) ON DELETE CASCADE,
  ql_position_id       uuid NOT NULL REFERENCES ql_position(id) ON DELETE CASCADE,
  parameters           jsonb NOT NULL,
  render_asset_id      uuid REFERENCES asset(id),
  analysis             jsonb NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (audio_palette_revision_id, ql_position_id)
);

CREATE TABLE modifier_operation (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  sequence_no          integer NOT NULL CHECK (sequence_no >= 0),
  operation_name       text NOT NULL,
  operation_version    text NOT NULL,
  parameters           jsonb NOT NULL,
  input_asset_id       uuid NOT NULL REFERENCES asset(id),
  output_asset_id      uuid NOT NULL REFERENCES asset(id),
  deterministic        boolean NOT NULL,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (engagement_id, sequence_no, output_asset_id),
  CHECK (input_asset_id <> output_asset_id)
);

CREATE TABLE render_plan (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  storyboard_revision_id uuid NOT NULL REFERENCES storyboard_revision(id),
  art_direction_revision_id uuid NOT NULL REFERENCES art_direction_revision(id),
  symbol_revision_id   uuid NOT NULL REFERENCES symbol_revision(id),
  audio_palette_revision_id uuid NOT NULL REFERENCES audio_palette_revision(id),
  profile              text NOT NULL,
  plan                 jsonb NOT NULL,
  plan_hash            char(64) NOT NULL CHECK (plan_hash ~ '^[0-9a-f]{64}$'),
  renderer             text NOT NULL,
  renderer_version     text NOT NULL,
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (engagement_id, plan_hash)
);

CREATE TABLE rendition (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  render_plan_id       uuid NOT NULL REFERENCES render_plan(id),
  rendition_kind       text NOT NULL CHECK (rendition_kind IN (
    'web_card', 'master_video', 'loop_video', 'poster', 'audio_master',
    'print_front', 'print_back', 'transparent_symbol', 'social_variant'
  )),
  profile              text NOT NULL,
  revision_no          integer NOT NULL CHECK (revision_no > 0),
  status               text NOT NULL CHECK (status IN ('rendering', 'candidate', 'approved', 'superseded', 'failed')),
  manifest             jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (engagement_id, rendition_kind, profile, revision_no)
);

CREATE TABLE rendition_asset (
  rendition_id         uuid NOT NULL REFERENCES rendition(id) ON DELETE CASCADE,
  asset_id             uuid NOT NULL REFERENCES asset(id),
  role                 text NOT NULL,
  PRIMARY KEY (rendition_id, asset_id, role)
);

CREATE TABLE action_definition (
  name                 text NOT NULL,
  version              text NOT NULL,
  side_effect          action_side_effect NOT NULL,
  input_schema_ref     text NOT NULL,
  output_schema_ref    text NOT NULL,
  required_permissions text[] NOT NULL,
  provider_dependencies text[] NOT NULL DEFAULT '{}',
  audit_required       boolean NOT NULL DEFAULT true,
  gate_mode            action_gate_mode NOT NULL DEFAULT 'none',
  gate_policy          jsonb NOT NULL DEFAULT '{"summary":"none","gates":[]}'::jsonb,
  idempotency_policy   text NOT NULL,
  retry_policy         jsonb NOT NULL,
  transaction_policy   text NOT NULL,
  PRIMARY KEY (name, version)
);

CREATE TABLE action_run (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  action_name          text NOT NULL,
  action_version       text NOT NULL,
  request_id           uuid NOT NULL UNIQUE,
  idempotency_key      text NOT NULL,
  actor_id             uuid NOT NULL REFERENCES actor(id),
  session_id           uuid REFERENCES epi_session(id),
  engagement_id        uuid REFERENCES engagement(id),
  status               action_run_status NOT NULL DEFAULT 'queued',
  input                jsonb NOT NULL,
  output               jsonb,
  warning_set          jsonb NOT NULL DEFAULT '[]'::jsonb,
  next_actions         jsonb NOT NULL DEFAULT '[]'::jsonb,
  retry_metadata       jsonb NOT NULL DEFAULT '{}'::jsonb,
  resume_cursor        jsonb,
  started_at           timestamptz,
  completed_at         timestamptz,
  created_at           timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (action_name, action_version) REFERENCES action_definition(name, version),
  UNIQUE (action_name, action_version, idempotency_key)
);
CREATE INDEX action_run_engagement_idx ON action_run (engagement_id, created_at);
CREATE INDEX action_run_status_idx ON action_run (status, created_at);

CREATE TABLE action_event (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  action_run_id        uuid NOT NULL REFERENCES action_run(id) ON DELETE CASCADE,
  sequence_no          bigint NOT NULL,
  event_type           text NOT NULL,
  payload              jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at           timestamptz NOT NULL DEFAULT now(),
  UNIQUE (action_run_id, sequence_no)
);

CREATE TABLE action_gate_evaluation (
  id                         uuid PRIMARY KEY DEFAULT uuidv7(),
  action_run_id              uuid NOT NULL REFERENCES action_run(id) ON DELETE CASCADE,
  gate_index                 smallint NOT NULL CHECK (gate_index >= 0),
  evaluation_no              integer NOT NULL CHECK (evaluation_no > 0),
  gate_kind                  action_gate_kind NOT NULL,
  gate_stage                 action_gate_stage NOT NULL,
  gate_mode                  action_gate_mode NOT NULL,
  when_predicate             text NOT NULL,
  when_arguments             jsonb NOT NULL DEFAULT '{}'::jsonb,
  when_result                boolean NOT NULL,
  requires_predicate         text NOT NULL,
  requires_arguments         jsonb NOT NULL DEFAULT '{}'::jsonb,
  requires_result            boolean NOT NULL,
  decision                   action_gate_decision NOT NULL,
  failure_code               text,
  context_hash               char(64) NOT NULL,
  predicate_registry_version text NOT NULL,
  evaluator_version          text NOT NULL,
  evaluated_at               timestamptz NOT NULL DEFAULT now(),
  UNIQUE (action_run_id, gate_index, evaluation_no),
  CHECK (
    (decision='not_applicable' AND when_result=false)
    OR (decision='passed' AND when_result=true AND requires_result=true)
    OR (decision='blocked' AND when_result=true AND requires_result=false)
  ),
  CHECK (decision<>'blocked' OR failure_code IS NOT NULL)
);
CREATE INDEX action_gate_run_stage_idx ON action_gate_evaluation(action_run_id, gate_stage, gate_index, evaluation_no DESC);

CREATE TABLE provider_disclosure_manifest (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  action_run_id        uuid REFERENCES action_run(id) ON DELETE SET NULL,
  provider_job_id      uuid REFERENCES provider_job(id) ON DELETE SET NULL,
  projection_id        uuid NOT NULL REFERENCES engagement_projection(id),
  provider             text NOT NULL,
  model_id             text,
  purpose              text NOT NULL,
  transmitted_field_paths text[] NOT NULL DEFAULT '{}',
  transmitted_asset_ids uuid[] NOT NULL DEFAULT '{}',
  privacy_summary      jsonb NOT NULL,
  retention_expectation jsonb NOT NULL,
  consent_receipt      jsonb NOT NULL,
  status               text NOT NULL CHECK (status IN ('proposed', 'approved', 'rejected', 'used', 'expired')),
  created_by           uuid REFERENCES actor(id),
  approved_by          uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  approved_at          timestamptz,
  used_at              timestamptz,
  CHECK (status NOT IN ('approved','used') OR approved_at IS NOT NULL)
);
CREATE INDEX provider_disclosure_action_idx ON provider_disclosure_manifest(action_run_id);
CREATE INDEX provider_disclosure_job_idx ON provider_disclosure_manifest(provider_job_id);

CREATE TABLE audit_tick (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  action_run_id        uuid UNIQUE REFERENCES action_run(id) ON DELETE CASCADE,
  parent_tick_id       uuid REFERENCES audit_tick(id),
  subject_kind         text NOT NULL,
  subject_id           uuid,
  threshold            jsonb NOT NULL,
  selected_outcome     jsonb,
  rejected_candidates  jsonb NOT NULL DEFAULT '[]'::jsonb,
  remaining_uncertainty jsonb NOT NULL DEFAULT '[]'::jsonb,
  semantic_delta       jsonb NOT NULL DEFAULT '{}'::jsonb,
  media_delta          jsonb NOT NULL DEFAULT '{}'::jsonb,
  next_ground          jsonb,
  status               text NOT NULL CHECK (status IN ('open', 'complete', 'invalidated')),
  created_at           timestamptz NOT NULL DEFAULT now(),
  completed_at         timestamptz,
  CHECK (parent_tick_id IS NULL OR parent_tick_id <> id)
);

CREATE TABLE audit_position (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  audit_tick_id        uuid NOT NULL REFERENCES audit_tick(id) ON DELETE CASCADE,
  phase                ql_phase NOT NULL,
  position_index       smallint NOT NULL CHECK (position_index BETWEEN 0 AND 5),
  address              text GENERATED ALWAYS AS (
    CASE phase
      WHEN 'bimba' THEN 'P' || position_index::text
      ELSE 'P' || position_index::text || '′'
    END
  ) STORED,
  audit_role           text NOT NULL,
  content              jsonb NOT NULL,
  occupancy            ql_occupancy NOT NULL DEFAULT 'present',
  occupancy_reason     text,
  confidence           numeric(6,5) CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
  register             evidence_register NOT NULL,
  UNIQUE (audit_tick_id, phase, position_index),
  UNIQUE (audit_tick_id, address),
  CHECK (occupancy NOT IN ('missing', 'withheld', 'unknown') OR occupancy_reason IS NOT NULL)
);

CREATE TABLE approval (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  target_kind          text NOT NULL,
  target_id            uuid NOT NULL,
  approval_type        text NOT NULL,
  status               approval_status NOT NULL DEFAULT 'requested',
  requested_by         uuid REFERENCES actor(id),
  decided_by           uuid REFERENCES actor(id),
  request_note         text,
  decision_note        text,
  requested_at         timestamptz NOT NULL DEFAULT now(),
  decided_at           timestamptz,
  UNIQUE (target_kind, target_id, approval_type, requested_at)
);

CREATE TABLE validation_report (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  target_kind          text NOT NULL,
  target_id            uuid NOT NULL,
  validator_name       text NOT NULL,
  validator_version    text NOT NULL,
  passed               boolean NOT NULL,
  report_asset_id      uuid REFERENCES asset(id),
  receipt              jsonb NOT NULL,
  created_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE validation_finding (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  validation_report_id uuid NOT NULL REFERENCES validation_report(id) ON DELETE CASCADE,
  severity             validation_severity NOT NULL,
  code                 text NOT NULL,
  path                 text,
  message              text NOT NULL,
  evidence             jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE okf_export (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  projection_id        uuid NOT NULL REFERENCES engagement_projection(id),
  okf_version          text NOT NULL DEFAULT '0.2',
  disclosure           disclosure_class NOT NULL,
  bundle_asset_id      uuid NOT NULL REFERENCES asset(id),
  manifest             jsonb NOT NULL,
  manifest_hash        char(64) NOT NULL CHECK (manifest_hash ~ '^[0-9a-f]{64}$'),
  validation_report_id uuid REFERENCES validation_report(id),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  CHECK (disclosure <> 'secret'),
  UNIQUE (engagement_id, projection_id, okf_version, manifest_hash)
);

CREATE TABLE package_export (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  engagement_revision_no integer NOT NULL CHECK (engagement_revision_no > 0),
  projection_id        uuid NOT NULL REFERENCES engagement_projection(id),
  projection_hash      char(64) NOT NULL CHECK (projection_hash ~ '^[0-9a-f]{64}$'),
  ql_frame_revision_id uuid NOT NULL REFERENCES ql_frame_revision(id),
  ql_frame_hash        char(64) NOT NULL CHECK (ql_frame_hash ~ '^[0-9a-f]{64}$'),
  profile_set_id       uuid NOT NULL REFERENCES profile_set(id),
  profile_set_hash     char(64) NOT NULL CHECK (profile_set_hash ~ '^[0-9a-f]{64}$'),
  okf_export_id        uuid NOT NULL REFERENCES okf_export(id),
  disclosure           disclosure_class NOT NULL,
  package_asset_id     uuid NOT NULL REFERENCES asset(id),
  sqlite_schema_version text NOT NULL,
  specification_hash   char(64) NOT NULL CHECK (specification_hash ~ '^[0-9a-f]{64}$'),
  manifest_schema_id   text NOT NULL DEFAULT 'urn:epi-card:schema:package-manifest:1.0.0'
                       CHECK (manifest_schema_id='urn:epi-card:schema:package-manifest:1.0.0'),
  manifest_hash        char(64) NOT NULL CHECK (manifest_hash ~ '^[0-9a-f]{64}$'),
  package_root_sha256  char(64) NOT NULL CHECK (package_root_sha256 ~ '^[0-9a-f]{64}$'),
  manifest             jsonb NOT NULL,
  validation_report_id uuid NOT NULL REFERENCES validation_report(id),
  created_by           uuid REFERENCES actor(id),
  created_at           timestamptz NOT NULL DEFAULT now(),
  CHECK (disclosure <> 'secret'),
  UNIQUE (package_root_sha256),
  UNIQUE (engagement_id, projection_id, ql_frame_revision_id, manifest_hash)
);

CREATE TABLE package_export_rendition (
  package_export_id    uuid NOT NULL REFERENCES package_export(id) ON DELETE CASCADE,
  rendition_id         uuid NOT NULL REFERENCES rendition(id),
  package_role         text NOT NULL,
  PRIMARY KEY (package_export_id, rendition_id, package_role)
);

CREATE OR REPLACE FUNCTION enforce_okf_export_consistency()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM engagement_projection p
    WHERE p.id=NEW.projection_id
      AND p.engagement_id=NEW.engagement_id
      AND p.status='approved'
      AND p.projection_kind IN ('private','shared','public')
      AND p.projection_kind=NEW.disclosure::text
  ) THEN
    RAISE EXCEPTION 'OKF export projection must be approved, non-provider, same-engagement, and disclosure-matched';
  END IF;
  IF NEW.validation_report_id IS NOT NULL AND NOT EXISTS (
    SELECT 1 FROM validation_report v
    WHERE v.id=NEW.validation_report_id
      AND v.engagement_id=NEW.engagement_id
      AND v.passed
  ) THEN
    RAISE EXCEPTION 'OKF export validation report must be passing and belong to the same engagement';
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER okf_export_consistency_guard
BEFORE INSERT OR UPDATE ON okf_export
FOR EACH ROW EXECUTE FUNCTION enforce_okf_export_consistency();

CREATE OR REPLACE FUNCTION enforce_package_export_consistency()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM engagement e
    WHERE e.id=NEW.engagement_id
      AND e.current_revision=NEW.engagement_revision_no
      AND e.current_ql_frame_revision_id=NEW.ql_frame_revision_id
      AND e.profile_set_id=NEW.profile_set_id
  ) THEN
    RAISE EXCEPTION 'Package export must freeze the current engagement revision, approved QL frame pointer, and active profile set';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM engagement_projection p
    WHERE p.id=NEW.projection_id
      AND p.engagement_id=NEW.engagement_id
      AND p.status='approved'
      AND p.projection_kind IN ('private','shared','public')
      AND p.projection_kind=NEW.disclosure::text
      AND p.snapshot_hash=NEW.projection_hash
  ) THEN
    RAISE EXCEPTION 'Package projection must be approved, non-provider, same-engagement, disclosure-matched, and hash-matched';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM ql_frame_revision q
    WHERE q.id=NEW.ql_frame_revision_id
      AND q.engagement_id=NEW.engagement_id
      AND q.status='approved'
      AND q.frame_hash=NEW.ql_frame_hash
  ) THEN
    RAISE EXCEPTION 'Package QL frame revision must be approved and belong to the same engagement';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM profile_set s
    WHERE s.id=NEW.profile_set_id AND s.status='active'
      AND s.set_hash=NEW.profile_set_hash
  ) THEN
    RAISE EXCEPTION 'Package profile set must be active';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM okf_export o
    JOIN validation_report ov ON ov.id=o.validation_report_id
    WHERE o.id=NEW.okf_export_id
      AND o.engagement_id=NEW.engagement_id
      AND o.projection_id=NEW.projection_id
      AND o.disclosure=NEW.disclosure
      AND ov.engagement_id=NEW.engagement_id
      AND ov.passed
  ) THEN
    RAISE EXCEPTION 'Package OKF export must use the same engagement, projection, and disclosure';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM validation_report v
    WHERE v.id=NEW.validation_report_id
      AND v.engagement_id=NEW.engagement_id
      AND v.passed
  ) THEN
    RAISE EXCEPTION 'Package validation report must be passing and belong to the same engagement';
  END IF;
  IF NOT EXISTS (
    SELECT 1 FROM schema_revision s
    WHERE s.version=NEW.sqlite_schema_version
      AND s.specification_hash=NEW.specification_hash
  ) THEN
    RAISE EXCEPTION 'Package specification hash must match an installed schema revision';
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER package_export_consistency_guard
BEFORE INSERT OR UPDATE ON package_export
FOR EACH ROW EXECUTE FUNCTION enforce_package_export_consistency();

CREATE OR REPLACE FUNCTION enforce_package_rendition_consistency()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM package_export p
    JOIN rendition r ON r.id=NEW.rendition_id
    WHERE p.id=NEW.package_export_id
      AND r.engagement_id=p.engagement_id
      AND r.status='approved'
  ) THEN
    RAISE EXCEPTION 'Packaged rendition must be approved and belong to the package engagement';
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER package_export_rendition_consistency_guard
BEFORE INSERT OR UPDATE ON package_export_rendition
FOR EACH ROW EXECUTE FUNCTION enforce_package_rendition_consistency();

CREATE TABLE publication (
  id                   uuid PRIMARY KEY DEFAULT uuidv7(),
  engagement_id        uuid NOT NULL REFERENCES engagement(id) ON DELETE CASCADE,
  rendition_id         uuid NOT NULL REFERENCES rendition(id),
  platform             text NOT NULL,
  account_ref          text NOT NULL,
  status               publication_status NOT NULL DEFAULT 'prepared',
  metadata             jsonb NOT NULL,
  disclosure_manifest  jsonb NOT NULL,
  approval_id          uuid REFERENCES approval(id),
  remote_publication_id text,
  remote_status        jsonb NOT NULL DEFAULT '{}'::jsonb,
  idempotency_key      text NOT NULL,
  prepared_at          timestamptz NOT NULL DEFAULT now(),
  submitted_at         timestamptz,
  published_at         timestamptz,
  UNIQUE (platform, account_ref, idempotency_key)
);

-- ---------------------------------------------------------------------------
-- Canonical QL seed and validators
-- ---------------------------------------------------------------------------

CREATE TABLE ql_canonical_position (
  phase                ql_phase NOT NULL,
  position_index       smallint NOT NULL CHECK (position_index BETWEEN 0 AND 5),
  address              text NOT NULL UNIQUE,
  canonical_unit       text NOT NULL,
  canonical_question   text NOT NULL,
  structural_role      text NOT NULL,
  PRIMARY KEY (phase, position_index),
  CHECK (
    (phase='bimba' AND address='P' || position_index::text)
    OR
    (phase='pratibimba' AND address='P' || position_index::text || '′')
  )
);

INSERT INTO ql_canonical_position VALUES
  ('bimba',0,'P0','Truth','Why?','Ground / source / ever-present origin'),
  ('bimba',1,'P1','Mind','What?','First definition / material articulation'),
  ('bimba',2,'P2','Word','How?','Dynamis / operation / energetic expression'),
  ('bimba',3,'P3','Logos','Who? Which? Whereby?','Pattern / identity / ordering relation'),
  ('bimba',4,'P4','Son','Where? When? Whither?','Context / horizon / situated embodiment'),
  ('bimba',5,'P5','Image','Why-for? Why-not?','Synthesis / integration / manifested whole'),
  ('pratibimba',0,'P0′','Play','Why, through groundlessness?','Abyss, freedom, ungrounded source condition'),
  ('pratibimba',1,'P1′','Need','What hidden form or trace remains?','Residue, evidence, demand, concealed definition'),
  ('pratibimba',2,'P2′','Sacrifice','How does operation meet obstruction and cost?','Resistance, shadow, exchange, necessary loss'),
  ('pratibimba',3,'P3′','Decision','Which pattern operates beneath the recognised pattern?','Cut, counter-pattern, recurrence, governing choice'),
  ('pratibimba',4,'P4′','Love','Which sources and missed contexts reopen the horizon?','Context examining itself, care, embrace, reframing'),
  ('pratibimba',5,'P5′','Work','What crystallises from the conjugate passage?','Verified expression, public work, completed recognition');

ALTER TABLE ql_canonical_position
  ADD CONSTRAINT ql_canonical_position_full_unique
  UNIQUE (phase, position_index, address, canonical_unit, canonical_question, structural_role);

ALTER TABLE ql_position
  ADD CONSTRAINT ql_position_canonical_identity_fk
  FOREIGN KEY (phase, position_index, address, canonical_unit, canonical_question, structural_role)
  REFERENCES ql_canonical_position(phase, position_index, address, canonical_unit, canonical_question, structural_role);

CREATE TABLE audit_canonical_position (
  phase                ql_phase NOT NULL,
  position_index       smallint NOT NULL CHECK (position_index BETWEEN 0 AND 5),
  audit_role           text NOT NULL,
  PRIMARY KEY (phase, position_index),
  UNIQUE (phase, position_index, audit_role)
);

INSERT INTO audit_canonical_position VALUES
  ('bimba',0,'decision_ground'),
  ('bimba',1,'objective_or_candidate_field'),
  ('bimba',2,'proposed_operation'),
  ('bimba',3,'selection_pattern_or_test'),
  ('bimba',4,'situated_constraints'),
  ('bimba',5,'provisional_integrated_outcome'),
  ('pratibimba',0,'ungrounded_assumptions_and_unknowns'),
  ('pratibimba',1,'traces_evidence_and_provenance'),
  ('pratibimba',2,'obstruction_failure_cost_or_sacrifice'),
  ('pratibimba',3,'counter_pattern_or_hidden_bias'),
  ('pratibimba',4,'missed_context_or_wider_horizon'),
  ('pratibimba',5,'verified_work_and_deposited_output');

ALTER TABLE audit_position
  ADD CONSTRAINT audit_position_canonical_role_fk
  FOREIGN KEY (phase, position_index, audit_role)
  REFERENCES audit_canonical_position(phase, position_index, audit_role);

CREATE OR REPLACE FUNCTION guard_ql_frame_revision_immutable()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF TG_OP='DELETE' AND OLD.status IN ('approved','superseded') THEN
    RAISE EXCEPTION 'Approved/superseded QL frame revision % is immutable', OLD.id;
  END IF;
  IF TG_OP='UPDATE' AND OLD.status IN ('approved','superseded') THEN
    IF NEW.engagement_id IS DISTINCT FROM OLD.engagement_id
       OR NEW.revision_no IS DISTINCT FROM OLD.revision_no
       OR NEW.prior_revision_id IS DISTINCT FROM OLD.prior_revision_id
       OR NEW.threshold_snapshot IS DISTINCT FROM OLD.threshold_snapshot
       OR NEW.frame_snapshot IS DISTINCT FROM OLD.frame_snapshot
       OR NEW.frame_hash IS DISTINCT FROM OLD.frame_hash
       OR NEW.created_by IS DISTINCT FROM OLD.created_by
       OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN
      RAISE EXCEPTION 'Approved/superseded QL frame revision % content is immutable', OLD.id;
    END IF;
  END IF;
  RETURN CASE WHEN TG_OP='DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE TRIGGER ql_frame_revision_immutable_guard
BEFORE UPDATE OR DELETE ON ql_frame_revision
FOR EACH ROW EXECUTE FUNCTION guard_ql_frame_revision_immutable();

CREATE OR REPLACE FUNCTION initialize_ql_frame(p_engagement_id uuid)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO ql_position (
    engagement_id, phase, position_index,
    canonical_unit, canonical_question, structural_role,
    occupancy, occupancy_reason
  )
  SELECT
    p_engagement_id, phase, position_index,
    canonical_unit, canonical_question, structural_role,
    'unknown'::ql_occupancy, 'Not yet mapped'
  FROM ql_canonical_position
  ON CONFLICT (engagement_id, phase, position_index) DO NOTHING;

  -- Directed adjacency within each phase.
  INSERT INTO ql_relation (engagement_id, source_position_id, target_position_id, relation_type, direction, sequence_no)
  SELECT p_engagement_id, a.id, b.id, 'adjacent', 'directed', a.position_index
  FROM ql_position a
  JOIN ql_position b
    ON b.engagement_id = a.engagement_id
   AND b.phase = a.phase
   AND b.position_index = a.position_index + 1
  WHERE a.engagement_id = p_engagement_id
  ON CONFLICT DO NOTHING;

  -- Klein twist P5 -> P0′.
  INSERT INTO ql_relation (engagement_id, source_position_id, target_position_id, relation_type, direction, sequence_no)
  SELECT p_engagement_id, a.id, b.id, 'klein_twist', 'directed', 6
  FROM ql_position a, ql_position b
  WHERE a.engagement_id=p_engagement_id AND b.engagement_id=p_engagement_id
    AND a.phase='bimba' AND a.position_index=5
    AND b.phase='pratibimba' AND b.position_index=0
  ON CONFLICT DO NOTHING;

  -- Conjugate pairs.
  INSERT INTO ql_relation (engagement_id, source_position_id, target_position_id, relation_type, direction, sequence_no)
  SELECT p_engagement_id, b.id, p.id, 'conjugate', 'undirected', b.position_index
  FROM ql_position b
  JOIN ql_position p
    ON p.engagement_id=b.engagement_id
   AND p.phase='pratibimba'
   AND p.position_index=b.position_index
  WHERE b.engagement_id=p_engagement_id AND b.phase='bimba'
  ON CONFLICT DO NOTHING;

  -- Complement pairs in both phases: indices sum to 5.
  INSERT INTO ql_relation (engagement_id, source_position_id, target_position_id, relation_type, direction, sequence_no)
  SELECT p_engagement_id, a.id, b.id, 'complement', 'undirected', a.position_index
  FROM ql_position a
  JOIN ql_position b
    ON b.engagement_id=a.engagement_id
   AND b.phase=a.phase
   AND b.position_index=5-a.position_index
  WHERE a.engagement_id=p_engagement_id AND a.position_index < b.position_index
  ON CONFLICT DO NOTHING;
END;
$$;

CREATE OR REPLACE FUNCTION ql_frame_errors(p_engagement_id uuid)
RETURNS TABLE(code text, detail text)
LANGUAGE sql
AS $$
  WITH counts AS (
    SELECT
      count(*) AS total,
      count(*) FILTER (WHERE phase='bimba') AS bimba_count,
      count(*) FILTER (WHERE phase='pratibimba') AS pratibimba_count
    FROM ql_position WHERE engagement_id=p_engagement_id
  ), missing_return AS (
    SELECT NOT EXISTS (SELECT 1 FROM return_deposit WHERE engagement_id=p_engagement_id) AS absent
  ), missing_sources AS (
    SELECT count(*) AS n
    FROM source_member sm
    JOIN source_form sf ON sf.id=sm.source_form_id
    WHERE sf.engagement_id=p_engagement_id
      AND NOT EXISTS (
        SELECT 1 FROM ql_assignment qa WHERE qa.source_member_id=sm.id
      )
  )
  SELECT 'QL_POSITION_COUNT', format('Expected 12 positions; found %s', total)
    FROM counts WHERE total<>12
  UNION ALL
  SELECT 'QL_BIMBA_COUNT', format('Expected 6 Bimba positions; found %s', bimba_count)
    FROM counts WHERE bimba_count<>6
  UNION ALL
  SELECT 'QL_PRATIBIMBA_COUNT', format('Expected 6 Pratibimba positions; found %s', pratibimba_count)
    FROM counts WHERE pratibimba_count<>6
  UNION ALL
  SELECT 'QL_RETURN_MISSING', 'Return deposit 5′→0⁺ is missing'
    FROM missing_return WHERE absent
  UNION ALL
  SELECT 'QL_APPROVED_REVISION_MISSING', 'An approved immutable QL frame revision is not selected'
    WHERE NOT EXISTS (
      SELECT 1
      FROM engagement e
      JOIN ql_frame_revision r ON r.id=e.current_ql_frame_revision_id
      WHERE e.id=p_engagement_id AND r.engagement_id=e.id AND r.status='approved'
    )
  UNION ALL
  SELECT 'PROFILE_SET_MISSING', 'A versioned profile set is not selected'
    WHERE NOT EXISTS (SELECT 1 FROM engagement e WHERE e.id=p_engagement_id AND e.profile_set_id IS NOT NULL)
  UNION ALL
  SELECT 'SOURCE_MEMBER_UNASSIGNED', format('%s source members lack an explicit assignment, including unassigned', n)
    FROM missing_sources WHERE n>0;
$$;

CREATE OR REPLACE FUNCTION assert_engagement_finalizable(p_engagement_id uuid)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
  v_errors text;
BEGIN
  SELECT string_agg(code || ': ' || detail, E'\n') INTO v_errors
  FROM ql_frame_errors(p_engagement_id);

  IF v_errors IS NOT NULL THEN
    RAISE EXCEPTION 'Engagement % is not finalizable:%', p_engagement_id, E'\n' || v_errors;
  END IF;
END;
$$;

CREATE OR REPLACE FUNCTION guard_engagement_status_transition()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.status IN ('approved','rendered','published','returned')
     AND NEW.status IS DISTINCT FROM OLD.status THEN
    PERFORM assert_engagement_finalizable(NEW.id);
  END IF;
  NEW.updated_at := now();
  RETURN NEW;
END;
$$;

CREATE TRIGGER engagement_status_guard
BEFORE UPDATE OF status ON engagement
FOR EACH ROW EXECUTE FUNCTION guard_engagement_status_transition();

CREATE OR REPLACE FUNCTION audit_tick_errors(p_tick_id uuid)
RETURNS TABLE(code text, detail text)
LANGUAGE sql
AS $$
  WITH counts AS (
    SELECT
      count(*) AS total,
      count(*) FILTER (WHERE phase='bimba') AS bimba_count,
      count(*) FILTER (WHERE phase='pratibimba') AS pratibimba_count
    FROM audit_position WHERE audit_tick_id=p_tick_id
  ), ret AS (
    SELECT selected_outcome IS NULL OR next_ground IS NULL AS invalid
    FROM audit_tick WHERE id=p_tick_id
  )
  SELECT 'AUDIT_POSITION_COUNT', format('Expected 12 audit positions; found %s', total)
    FROM counts WHERE total<>12
  UNION ALL
  SELECT 'AUDIT_BIMBA_COUNT', format('Expected 6 Bimba audit positions; found %s', bimba_count)
    FROM counts WHERE bimba_count<>6
  UNION ALL
  SELECT 'AUDIT_PRATIBIMBA_COUNT', format('Expected 6 Pratibimba audit positions; found %s', pratibimba_count)
    FROM counts WHERE pratibimba_count<>6
  UNION ALL
  SELECT 'AUDIT_RETURN_INCOMPLETE', 'selected_outcome and next_ground are required'
    FROM ret WHERE invalid;
$$;

CREATE OR REPLACE FUNCTION action_gate_errors(p_run_id uuid)
RETURNS TABLE(code text, detail text)
LANGUAGE sql
AS $$
  WITH definition AS (
    SELECT ad.gate_policy
    FROM action_run ar
    JOIN action_definition ad ON ad.name=ar.action_name AND ad.version=ar.action_version
    WHERE ar.id=p_run_id
  ), defined AS (
    SELECT (x.ordinality-1)::smallint AS gate_index, x.gate->>'stage' AS gate_stage
    FROM definition d,
         jsonb_array_elements(COALESCE(d.gate_policy->'gates','[]'::jsonb)) WITH ORDINALITY AS x(gate, ordinality)
    WHERE x.gate->>'stage' IN ('pre_execute','pre_commit','pre_publish')
  ), latest AS (
    SELECT DISTINCT ON (gate_index, gate_stage)
           gate_index, gate_stage::text, decision::text, failure_code
    FROM action_gate_evaluation
    WHERE action_run_id=p_run_id
    ORDER BY gate_index, gate_stage, evaluation_no DESC
  )
  SELECT 'GATE_EVALUATION_MISSING', format('Gate %s at %s has no evaluation', d.gate_index, d.gate_stage)
  FROM defined d
  LEFT JOIN latest l ON l.gate_index=d.gate_index AND l.gate_stage=d.gate_stage
  WHERE l.gate_index IS NULL
  UNION ALL
  SELECT COALESCE(l.failure_code,'GATE_BLOCKED'), format('Gate %s at %s is blocked', d.gate_index, d.gate_stage)
  FROM defined d
  JOIN latest l ON l.gate_index=d.gate_index AND l.gate_stage=d.gate_stage
  WHERE l.decision='blocked';
$$;

CREATE OR REPLACE FUNCTION guard_action_success()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  v_audit_required boolean;
  v_tick_id uuid;
  v_errors text;
  v_gate_errors text;
BEGIN
  IF NEW.status='succeeded' AND NEW.status IS DISTINCT FROM OLD.status THEN
    SELECT audit_required INTO v_audit_required
    FROM action_definition
    WHERE name=NEW.action_name AND version=NEW.action_version;

    IF v_audit_required THEN
      SELECT id INTO v_tick_id FROM audit_tick WHERE action_run_id=NEW.id;
      IF v_tick_id IS NULL THEN
        RAISE EXCEPTION 'Action run % requires a QL audit tick', NEW.id;
      END IF;
      SELECT string_agg(code || ': ' || detail, E'\n') INTO v_errors
      FROM audit_tick_errors(v_tick_id);
      IF v_errors IS NOT NULL THEN
        RAISE EXCEPTION 'Action run % audit is incomplete:%', NEW.id, E'\n' || v_errors;
      END IF;
      UPDATE audit_tick SET status='complete', completed_at=COALESCE(completed_at, now()) WHERE id=v_tick_id;
    END IF;

    SELECT string_agg(code || ': ' || detail, E'\n') INTO v_gate_errors
    FROM action_gate_errors(NEW.id);
    IF v_gate_errors IS NOT NULL THEN
      RAISE EXCEPTION 'Action run % has unsatisfied gates:%', NEW.id, E'\n' || v_gate_errors;
    END IF;

    NEW.completed_at := COALESCE(NEW.completed_at, now());
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER action_success_guard
BEFORE UPDATE OF status ON action_run
FOR EACH ROW EXECUTE FUNCTION guard_action_success();

CREATE OR REPLACE FUNCTION validate_storyboard_shape(p_storyboard_id uuid)
RETURNS TABLE(code text, detail text)
LANGUAGE sql
AS $$
  WITH pairs AS (
    SELECT count(*) AS n FROM scene_pair WHERE storyboard_revision_id=p_storyboard_id
  ), atoms AS (
    SELECT count(*) AS n
    FROM scene_atom sa
    JOIN scene_pair sp ON sp.id=sa.scene_pair_id
    WHERE sp.storyboard_revision_id=p_storyboard_id
  ), coverage AS (
    SELECT count(DISTINCT qp.address) AS n
    FROM scene_atom sa
    JOIN scene_pair sp ON sp.id=sa.scene_pair_id
    JOIN ql_position qp ON qp.id=sa.ql_position_id
    WHERE sp.storyboard_revision_id=p_storyboard_id
  )
  SELECT 'SCENE_PAIR_COUNT', format('Expected 6 scene pairs; found %s', n) FROM pairs WHERE n<>6
  UNION ALL
  SELECT 'SCENE_ATOM_COUNT', format('Expected 12 scene atoms; found %s', n) FROM atoms WHERE n<>12
  UNION ALL
  SELECT 'SCENE_POSITION_COVERAGE', format('Expected 12 distinct QL addresses; found %s', n) FROM coverage WHERE n<>12;
$$;

CREATE INDEX ql_assignment_source_idx ON ql_assignment (source_member_id);
CREATE UNIQUE INDEX ql_assignment_unassigned_once_idx ON ql_assignment(source_member_id) WHERE role='unassigned';
CREATE INDEX claim_position_idx ON claim (ql_position_id, status);
CREATE INDEX resonance_position_idx ON resonance_state (engagement_id, ql_position_id);
CREATE INDEX scene_atom_position_idx ON scene_atom (ql_position_id);
CREATE INDEX audit_position_tick_order_idx ON audit_position (audit_tick_id, phase, position_index);
CREATE INDEX publication_status_idx ON publication (status, prepared_at);

INSERT INTO schema_revision(version, specification_hash, notes)
VALUES ('1.0.0', 'dfdaa496ef90261ba185510f2b65abde88e0ee6059dfd3fbbd47b7be3b07a902', 'Packaged against the normative v1.0.0 specification.')
ON CONFLICT (version) DO NOTHING;

COMMIT;
