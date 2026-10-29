{% set dimensions_fields = [
        ('width', 'numeric'),
        ('height', 'numeric'),
        ('depth', 'numeric')
        ]
 %}

{% set reviews_fields = [
        ('rating', 'numeric'),
        ('comment', 'text'),
        ('date', 'timestamptz'),
        ('reviewerName', 'text'),
        ('reviewerEmail', 'text')
    ]
%}

{% set dimensions_column_name = 'dimensions'%}

{% set reviews_column_name = 'reviews'%}

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
    
    from {{ source('raw', 'products') }} source

    where source.ingestion_timestamp > (

        select max_ingestion_timestamp

        from watermak

        )

),exploded as (

    select
        id as product_id,
        title,
        category,
        price,
        "discountPercentage" as discountpercentage,
        stock,
        brand,
        {% for field_name, field_type in dimensions_fields  %}

        {{ extract_json_object_field(dimensions_column_name, field_name, field_type) }} as {{ field_name }}

            {% if not loop.last %},
    
            {% endif %}

        {% endfor %},
        "shippingInformation" as shippinginformation,
        "availabilityStatus" as availabilitystatus,
        jsonb_array_elements(reviews::jsonb) as reviews,
        "returnPolicy" as returnpolicy,
        "minimumOrderQuantity" as minimumorderquantity,
        thumbnail,
        ingestion_timestamp
    from new_records

),

decompressed as (

    select 

        product_id,
        title,
        category,
        price,
        discountpercentage,
        stock,
        brand,
        width,
        height,
        depth,

        shippinginformation,
        availabilitystatus,

        {% for field_name, field_type in reviews_fields  %}

            {{ extract_json_fields(reviews_column_name, field_name, field_type) }} as {{ field_name }}

            {% if not loop.last %},
    
            {% endif %}

        {% endfor %},

        returnpolicy,
        minimumorderquantity,
        thumbnail,
        ingestion_timestamp

    from exploded

),

filtred_rows as (

    select 
        *,
        row_number() over (partition by product_id order by "date" desc) as row_num

    from decompressed

)

select 

    product_id,
    title,
    category,
    price,
    discountpercentage,
    stock,
    brand,
    width,
    height,
    depth,

    shippinginformation,
    availabilitystatus,

    rating,
    comment,
    "date" as reviewdate,
    reviewername,
    revieweremail,

    returnpolicy,
    minimumorderquantity,
    thumbnail,
    ingestion_timestamp

from filtred_rows

where row_num = 1