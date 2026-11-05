select *
from {{ ref('fct_sales') }}

where net_amount < 0