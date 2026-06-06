create or replace view fraud_detection_view as
select 
    v.transaction_id,
    v.user_id,
    v.voice_sample,
    v.timestamp,
    case 
        when a.voice_score < 0.5 then 'high risk'
        when a.voice_score >= 0.5 and a.voice_score < 0.8 then 'medium risk'
        else 'low risk'
    end as risk_level,
    a.confidence_score
from 
    voice_transactions v
join 
    voice_analysis a on v.transaction_id = a.transaction_id
where 
    v.timestamp >= now() - interval '30 days'
    and a.voice_score is not null
order by 
    risk_level desc, 
    a.confidence_score desc;

-- TODO: add more filters for specific user behaviors in the future
-- this view should help monitor and flag suspicious activities based on voice quality