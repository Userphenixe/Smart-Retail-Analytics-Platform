select *
from {{ ref('dim_recipe') }}

where avg_rating < 0
or avg_rating > 5