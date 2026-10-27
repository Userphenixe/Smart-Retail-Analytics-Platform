{% set fields = [
    ('id', 'numeric'),
    ('title', 'text'),
    ('price', 'numeric'),
    ('quantity', 'numeric'),
    ('total', 'numeric'),
    ('discountPercentage', 'numeric'),
    ('discountedTotal', 'numeric'),
    ('thumbnail', 'text'),
] %}

{% set column_name = 'product'%}

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
    
    from {{ source('raw', 'carts') }} source

    where source.ingestion_timestamp > (

        select max_ingestion_timestamp

        from watermak

        )
),

exploded as (

    select
        id as cart_id,
        jsonb_array_elements(products::jsonb) as product,
        "userId" as userid,
        ingestion_timestamp
    from new_records

)

select 

    cart_id,

    {% for field_name, field_type in fields  %}

    {{ extract_json_fields(column_name, field_name, field_type) }} as {{ field_name }}
    
    {% if not loop.last %},
    
    {% endif %}

    {% endfor %},

    userid,
    ingestion_timestamp

from exploded

