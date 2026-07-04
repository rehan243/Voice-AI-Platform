create or replace view fraud_detection as
select
    v.transaction_id,
    v.user_id,
    v.voiceprint_id,
    v.transaction_amount,
    v.transaction_date,
    case 
        when v.transaction_amount > 1000 then 'high_value'
        when v.transaction_amount between 500 and 1000 then 'medium_value'
        else 'low_value'
    end as value_category,
    case 
        when v.voiceprint_id is null then 'unverified'
        when a.is_fraud = true then 'fraudulent'
        else 'verified'
    end as verification_status
from
    voice_transactions v
left join
    authentication_logs a on v.voiceprint_id = a.voiceprint_id
where
    v.transaction_date >= current_date - interval '30 days'
    and (a.is_fraud is not null or v.voiceprint_id is null)

-- this view helps in identifying transactions that might need further review
-- TODO: consider adding more filters based on user behavior
-- remember to check performance with larger datasets