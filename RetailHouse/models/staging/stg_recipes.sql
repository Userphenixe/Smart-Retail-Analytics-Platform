with watermak as (

    select 

        {% if is_incremental() %}

        max(ingestion_timestamp) as max_ingestion_timestamp
        from {{ this }}

        {% else %}

        cast('1900-01-01' as timestamp) as max_ingestion_timestamp
        
        {% endif %}
),

new_records as (

    select * 
    
    from {{ source('raw', 'recipes') }} source

    where source.ingestion_timestamp > (

        select max_ingestion_timestamp

        from watermak

        )

)

select

    id as recipe_id,
    "name" as recipe_name,
    "prepTimeMinutes" as prep_time_minutes,
    "cookTimeMinutes" as cook_time_minutes,
    servings,
    difficulty,
    cuisine,
    "caloriesPerServing" as calories_per_serving,
    "userId" as customer_id,
    rating,
    "reviewCount" as review_count,
    ingestion_timestamp

from new_records