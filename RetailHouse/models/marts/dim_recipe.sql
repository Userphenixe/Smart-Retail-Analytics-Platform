select 
    recipe_id,
    recipe_name,
    difficulty,
    difficulty_score,
    cuisine,
    avg_rating,
    review_count
from {{ref('int_recipes_enriched')}}
order by recipe_id