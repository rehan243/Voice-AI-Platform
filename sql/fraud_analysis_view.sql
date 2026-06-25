CREATE OR REPLACE VIEW fraud_analysis AS
SELECT 
    u.user_id,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_amount,
    AVG(t.amount) AS avg_transaction_amount,
    MAX(t.transaction_date) AS last_transaction_date,
    CASE 
        WHEN COUNT(t.transaction_id) > 10 THEN 'high_activity'
        WHEN COUNT(t.transaction_id) BETWEEN 5 AND 10 THEN 'medium_activity'
        ELSE 'low_activity'
    END AS activity_level
FROM 
    users u
JOIN 
    transactions t ON u.user_id = t.user_id
WHERE 
    t.transaction_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 
    u.user_id;

-- TODO: consider adding more filters based on transaction types or statuses

CREATE INDEX idx_fraud_user_id ON fraud_analysis(user_id);