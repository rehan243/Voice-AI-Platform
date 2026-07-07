-- this view analyzes voice interactions for potential fraud
-- based on certain keyword patterns and call durations

CREATE OR REPLACE VIEW voice_fraud_analysis AS
WITH keyword_matches AS (
    SELECT
        call_id,
        user_id,
        transcript,
        duration,
        CASE
            WHEN LOWER(transcript) LIKE '%fraud%' THEN 1
            ELSE 0
        END AS fraud_keyword
    FROM
        voice_calls
    WHERE
        processed = TRUE
),
aggregated_data AS (
    SELECT
        user_id,
        COUNT(CASE WHEN fraud_keyword = 1 THEN 1 END) AS fraud_count,
        AVG(duration) AS avg_duration
    FROM
        keyword_matches
    GROUP BY
        user_id
)
SELECT
    ud.user_id,
    ud.user_name,
    ad.fraud_count,
    ad.avg_duration
FROM
    user_details AS ud
JOIN
    aggregated_data AS ad ON ud.user_id = ad.user_id
WHERE
    ad.fraud_count > 0
ORDER BY
    ad.fraud_count DESC;

-- TODO: consider adding more filters or join conditions based on new requirements