{{
    config(
        materialized='view'
    )
}}


with calendar as (

    select
        generate_series(
            date '2025-01-01',
            date '2030-12-31',
            interval '1 day'
        )::date as date_day

)

select

    cast(to_char(date_day, 'YYYYMMDD') as integer)
        as date_key,

    date_day,

    extract(year from date_day)
        as year,

    concat(
        'Q',
        extract(quarter from date_day)
    ) as quarter,

    extract(month from date_day)
        as month,

    to_char(date_day, 'Month')
        as month_name,

    extract(week from date_day)
        as week_of_year,

    extract(day from date_day)
        as day_of_month,

    extract(isodow from date_day)
        as day_of_week,

    to_char(date_day, 'Day')
        as day_name,

    case
        when extract(isodow from date_day) in (6,7)
        then true
        else false
    end as is_weekend

from calendar