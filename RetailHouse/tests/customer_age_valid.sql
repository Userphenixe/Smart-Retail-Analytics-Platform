select *
from {{ ref('dim_customer') }}

where age < 0
or age > 120