select *
from {{ ref('fct_sales') }}

where discount_amount > gross_amount