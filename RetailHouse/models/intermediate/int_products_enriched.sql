select 
    product_id,
    title as product_name,
    sp.category,
    department,
    price,
    stock,
    availabilitystatus,
    is_available,
    round(
    width * height * depth,
    2
    )::numeric(10,2) as product_volume,
    rating
    from {{ ref('stg_products') }} sp
    inner join {{ ref('seed_product_categories') }} spc
        on sp.category = spc.category
    inner join {{ ref('seed_availability_status') }} sas
        on sp.availabilitystatus = sas.availability_status