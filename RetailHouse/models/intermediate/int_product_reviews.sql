select 
    product_id,
    rating,
    rating_band,
    comment,
    cast(concat(EXTRACT(YEAR FROM reviewdate), '-', EXTRACT(MONTH FROM reviewdate), '-', EXTRACT(DAY FROM reviewdate)) as date) as review_date,
    reviewername as reviewer_name
    from {{ ref('stg_products') }} sp
    inner join {{ ref('seed_rating_band') }} srb
        on sp.rating between srb.min_rating and srb.max_rating