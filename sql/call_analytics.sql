-- Call center / voice bot analytics. Tune retention with pg_partman or equivalent.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS calls (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    call_id         TEXT NOT NULL UNIQUE,
    tenant_id       UUID NOT NULL,
    direction       TEXT CHECK (direction IN ('inbound', 'outbound')),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at        TIMESTAMPTZ,
    agent_id        UUID,
    customer_ref    TEXT,
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_calls_tenant_started ON calls (tenant_id, started_at DESC);

CREATE TABLE IF NOT EXISTS transcripts (
    id          BIGSERIAL PRIMARY KEY,
    call_uuid   UUID NOT NULL REFERENCES calls (id) ON DELETE CASCADE,
    seq         INT NOT NULL,
    speaker     TEXT,
    text        TEXT NOT NULL,
    confidence  REAL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (call_uuid, seq)
);

CREATE INDEX IF NOT EXISTS idx_transcripts_call ON transcripts (call_uuid, seq);

CREATE TABLE IF NOT EXISTS sentiment_ticks (
    id             BIGSERIAL PRIMARY KEY,
    call_uuid      UUID NOT NULL REFERENCES calls (id) ON DELETE CASCADE,
    utterance_idx  INT NOT NULL,
    score          REAL NOT NULL,
    rolling_score  REAL,
    model          TEXT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sentiment_call ON sentiment_ticks (call_uuid, created_at);

CREATE TABLE IF NOT EXISTS dashboard_snapshots (
    bucket_start   TIMESTAMPTZ NOT NULL,
    tenant_id      UUID NOT NULL,
    active_calls   INT NOT NULL DEFAULT 0,
    negative_ratio REAL,
    avg_duration_s REAL,
    PRIMARY KEY (bucket_start, tenant_id)
);
