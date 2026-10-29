{%
    set fields = [
        ('currency', 'text'),
        ('cardType', 'text')
    ]
%}


{% set column_name = 'bank'%}

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
    
    from {{ source('raw', 'users') }} source

    where source.ingestion_timestamp > (

        select max_ingestion_timestamp

        from watermak

        )

),exploded as (

    select
        id as customer_id,
        "firstName" as firstname,
        "lastName" as lastname,
        username,
        gender,
        email,
        cast("birthDate" as date) as dateofbirth,

        {{ extract_json_object_field('address', 'city', 'text') }} as city,

        {% for field_name, field_type in fields %}

        {{ extract_json_object_field(column_name, field_name, field_type) }} as {{ field_name }}

            {% if not loop.last %},
    
            {% endif %}

        {% endfor %},

        {{ extract_json_object_field('company', 'department', 'text') }} as department,

        "role" as customer_role,
        ingestion_timestamp

    from new_records

)

select 

    customer_id,
    firstname,
    lastname,
    username,
    gender,
    email,
    dateofbirth,
    city,
    currency,
    cardtype,
    department,
    customer_role,
    ingestion_timestamp

from exploded