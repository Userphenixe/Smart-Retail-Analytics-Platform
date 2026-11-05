select 
    c.cart_id,
    ipe.product_id,
    c.title as product_name,
    c.price as product_price,
    c.quantity as product_quantity,
    c.discountpercentage,
    ipe.department as product_department,
    icp.full_name as customer_name
from {{ ref('stg_carts') }} c
inner join {{ ref('int_customer_profile') }} icp
    on c.userid = icp.customer_id
inner join {{ ref('int_products_enriched') }} ipe
    on c.id = ipe.product_id