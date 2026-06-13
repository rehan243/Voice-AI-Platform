-- this view analyzes potential fraudulent voice interactions
-- based on user behavior and interaction patterns

create or replace view fraud_analysis as
select 
    user_id,
    count(case when interaction_type = 'voice' then 1 end) as voice_interaction_count,
    count(case when interaction_type = 'text' then 1 end) as text_interaction_count,
    avg(interaction_duration) as average_duration,
    sum(case when is_fraudulent then 1 else 0 end) as total_fraudulent_interactions,
    (count(case when is_fraudulent then 1 else 0 end) * 100.0 / nullif(count(*), 0)) as fraud_percentage
from 
    voice_interactions
where 
    interaction_date >= current_date - interval '30 days'
group by 
    user_id
having 
    fraud_percentage > 5 -- threshold for flagging potential fraud

-- TODO: consider adding more filters or parameters for different time frames
-- this could help refine the analysis for specific use cases