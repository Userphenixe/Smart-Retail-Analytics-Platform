with customer_ages as (
    select
        customer_id,
        firstname,
        lastname,
        gender,
        cast(extract(year from age(current_date, dateofbirth)) as integer) as age,
        city
    from {{ ref('stg_customers') }}
)

select
    customer_id,
    concat(firstname, ' ', lastname) as full_name,
    gender,
    age,
    case
        when age < 18 then 'minor'
        when age between 18 and 24 then 'young adult'
        when age between 25 and 34 then 'adult'
        when age between 35 and 44 then 'middle-aged'
        when age between 45 and 54 then 'senior'
        when age between 55 and 64 then 'elderly'
        else 'centenarian'
    end as age_group,
    city as city_of_birth
from customer_ages