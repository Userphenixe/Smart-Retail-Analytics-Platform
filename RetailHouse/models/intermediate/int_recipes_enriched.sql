select 
    recipe_id,
    recipe_name,
    r.difficulty,
    d.difficulty_score,
    r.cuisine,
    r.customer_id,
    concat(c.firstname, ' ', c.lastname) as customer_name,
    r.rating as avg_rating,
    r.review_count
from {{ ref('stg_recipes') }} r
inner join {{ ref('seed_recipe_difficulty') }} d
    on r.difficulty = d.difficulty
inner join {{ ref('stg_customers') }} c
    on r.customer_id = c.customer_id