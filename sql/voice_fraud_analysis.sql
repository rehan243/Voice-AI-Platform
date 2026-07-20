-- this view aggregates voice call data to identify potential fraud patterns
-- we're focusing on calls with unusual durations and frequencies

create or replace view voice_fraud_analysis as
select 
    caller_id,
    count(*) as call_count,
    avg(call_duration) as avg_duration,
    stddev(call_duration) as duration_stddev,
    count(distinct callee_id) as unique_recipients
from 
    voice_calls
where 
    call_timestamp >= current_date - interval '30 days'
group by 
    caller_id
having 
    call_count > 20 
    and avg_duration > 120
    and duration_stddev > 30;

-- we might want to consider adding more metrics in the future
-- also, think about indexing the caller_id for better performance

-- let's test this view with some sample queries after creation
-- select * from voice_fraud_analysis where call_count > 50;