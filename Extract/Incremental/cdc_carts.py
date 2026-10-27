import json
import random
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://admin:admin@postgres:5432/analytics"
)


def simulate_carts_cdc(nb_records=5):

    carts_df = pd.read_sql(
        "select id from raw.carts",
        engine
    )

    products_df = pd.read_sql(
        """
        select
            id,
            title,
            price,
            "discountPercentage",
            thumbnail
        from raw.products
        """,
        engine
    )

    users_df = pd.read_sql(
        """
        select id
        from raw.users
        """,
        engine
    )

    max_cart_id = carts_df["id"].max()

    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")
    ingestion_timestamp = datetime.now()

    carts = []

    for i in range(nb_records):

        cart_id = int(max_cart_id) + i + 1

        user_id = int(
            users_df.sample(1)["id"].iloc[0]
        )

        nb_products = random.randint(1, 5)

        selected_products = products_df.sample(
            n=nb_products
        )

        cart_products = []

        total = 0
        discounted_total = 0
        total_quantity = 0

        for _, product in selected_products.iterrows():

            quantity = random.randint(1, 4)

            line_total = round(
                float(product["price"]) * quantity,
                2
            )

            line_discounted_total = round(
                line_total
                * (
                    1
                    - float(product["discountPercentage"]) / 100
                ),
                2
            )

            cart_products.append(
                {
                    "id": int(product["id"]),
                    "title": product["title"],
                    "price": float(product["price"]),
                    "quantity": quantity,
                    "total": line_total,
                    "discountPercentage": float(
                        product["discountPercentage"]
                    ),
                    "discountedTotal": line_discounted_total,
                    "thumbnail": product["thumbnail"]
                }
            )

            total += line_total
            discounted_total += line_discounted_total
            total_quantity += quantity

        carts.append(
            {
                "id": cart_id,
                "products": json.dumps(cart_products),
                "total": round(total, 2),
                "discountedTotal": round(
                    discounted_total,
                    2
                ),
                "userId": user_id,
                "totalProducts": len(cart_products),
                "totalQuantity": total_quantity,
                "batch_id": batch_id,
                "ingestion_timestamp": ingestion_timestamp,
                "source_system": "cdc_simulator"
            }
        )

    result_df = pd.DataFrame(carts)

    result_df.to_sql(
        "carts",
        con=engine,
        schema="raw",
        if_exists="append",
        index=False
    )

    print(
        f"{len(result_df)} carts inserted"
    )


if __name__ == "__main__":
    simulate_carts_cdc()