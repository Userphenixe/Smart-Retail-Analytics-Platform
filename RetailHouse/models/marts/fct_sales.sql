with sales as (

    select *
    from {{ ref('int_sales') }}

),

final as (

    select

        cart_id,

        customer_name,

        count(distinct product_id)
            as total_products,

        sum(product_quantity)
            as total_quantity,

        round(
            sum(
                product_quantity * product_price
            ),
            2
        ) as gross_amount,

        round(
            sum(
                (
                    product_quantity * product_price
                )
                *
                (
                    discountpercentage / 100
                )
            ),
            2
        ) as discount_amount,

        round(
            sum(
                (
                    product_quantity * product_price
                )
                -
                (
                    (
                        product_quantity * product_price
                    )
                    *
                    (
                        discountpercentage / 100
                    )
                )
            ),
            2
        ) as net_amount

    from sales

    group by
        cart_id,
        customer_name

)

select *
from final