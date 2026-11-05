select
    product_id,
    product_name,
    category,
    department,
    price,
    stock,
    int_product_reviews.rating,
    rating_band,
    review_date,
    reviewer_name
from {{ref('int_products_enriched')}}
inner join {{ref('int_product_reviews')}}
    using (product_id)
order by product_id, review_date desc