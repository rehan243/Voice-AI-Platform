-- rollups for exec dashboards without hammering raw call_fact
-- time filters are short on purpose so autovacuum does not fight huge seq scans

CREATE OR REPLACE VIEW v_call_duration_daily AS
SELECT date_trunc('day', started_at) AS day,
       count(*) AS calls,
       avg(duration_sec) AS avg_duration_sec,
       percentile_disc(0.9) WITHIN GROUP (ORDER BY duration_sec) AS p90_duration_sec
FROM call_fact
WHERE started_at > now() - interval '180 days'
GROUP BY 1;

CREATE OR REPLACE VIEW v_sentiment_trend_weekly AS
SELECT date_trunc('week', analyzed_at) AS week,
       avg(sentiment_score) AS avg_score,
       stddev_pop(sentiment_score) AS score_spread
FROM call_sentiment
WHERE analyzed_at > now() - interval '365 days'
GROUP BY 1;

CREATE OR REPLACE VIEW v_agent_performance AS
SELECT agent_id,
       count(*) AS handled_calls,
       avg(handle_time_sec) AS avg_handle_sec,
       sum(case when resolved then 1 else 0 end)::float / nullif(count(*), 0) AS resolve_rate
FROM call_handling
WHERE started_at > now() - interval '90 days'
GROUP BY agent_id;

CREATE OR REPLACE VIEW v_queue_wait_daily AS
SELECT date_trunc('day', enqueued_at) AS day,
       queue_name,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY wait_sec) AS p50_wait_sec,
       percentile_disc(0.95) WITHIN GROUP (ORDER BY wait_sec) AS p95_wait_sec
FROM call_queue_wait
WHERE enqueued_at > now() - interval '90 days'
GROUP BY 1, 2;

CREATE OR REPLACE VIEW v_transfer_rate_by_skill AS
SELECT skill,
       count(*) AS calls,
       sum(case when transferred then 1 else 0 end)::float / nullif(count(*), 0) AS transfer_rate
FROM call_routing
WHERE started_at > now() - interval '60 days'
GROUP BY skill;

-- indexes matter here because these views get hit by bi tools every morning
CREATE INDEX IF NOT EXISTS idx_call_fact_started ON call_fact (started_at);
CREATE INDEX IF NOT EXISTS idx_sentiment_time ON call_sentiment (analyzed_at);
CREATE INDEX IF NOT EXISTS idx_handling_agent ON call_handling (agent_id, started_at);
CREATE INDEX IF NOT EXISTS idx_queue_wait_day ON call_queue_wait (enqueued_at, queue_name);
CREATE INDEX IF NOT EXISTS idx_routing_skill ON call_routing (skill, started_at);
