select *
from {{ ref('int_products_enriched') }}

where product_volume <= 0