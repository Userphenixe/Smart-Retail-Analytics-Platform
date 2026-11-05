select 
    customer_id,
    full_name,
    gender,
    age,
    age_group,
    city_of_birth
from {{ref('int_customer_profile')}}
order by customer_id