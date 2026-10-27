import json
import random
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine


engine = create_engine(
    "postgresql+psycopg2://admin:admin@postgres:5432/analytics"
)


def simulate_recipes_cdc(nb_records=2):

    recipes_df = pd.read_sql(
        """
        select id
        from raw.recipes
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

    max_recipe_id = recipes_df["id"].max()

    cuisines = [
        "Italian",
        "Mexican",
        "Asian",
        "Mediterranean",
        "Moroccan",
        "Indian"
    ]

    meal_types = [
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snack"
    ]

    recipe_templates = [
        {
            "name": "Chicken Rice Bowl",
            "ingredients": [
                "Chicken breast",
                "Rice",
                "Olive oil",
                "Salt",
                "Pepper"
            ]
        },
        {
            "name": "Vegetable Pasta",
            "ingredients": [
                "Pasta",
                "Tomatoes",
                "Zucchini",
                "Olive oil",
                "Parmesan"
            ]
        },
        {
            "name": "Beef Tacos",
            "ingredients": [
                "Ground beef",
                "Tortillas",
                "Cheese",
                "Tomatoes",
                "Onions"
            ]
        },
        {
            "name": "Quinoa Salad",
            "ingredients": [
                "Quinoa",
                "Cucumber",
                "Tomatoes",
                "Feta cheese",
                "Olive oil"
            ]
        }
    ]

    rows = []

    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")
    ingestion_timestamp = datetime.now()

    for i in range(nb_records):

        recipe_id = int(max_recipe_id) + i + 1

        template = random.choice(recipe_templates)

        rows.append(
            {
                "id": recipe_id,
                "name": f"{template['name']} {recipe_id}",
                "ingredients": json.dumps(
                    template["ingredients"]
                ),
                "instructions": json.dumps(
                    [
                        "Prepare ingredients",
                        "Cook according to recipe",
                        "Serve and enjoy"
                    ]
                ),
                "prepTimeMinutes": random.randint(10, 30),
                "cookTimeMinutes": random.randint(10, 45),
                "servings": random.randint(2, 6),
                "difficulty": random.choice(
                    ["Easy", "Medium"]
                ),
                "cuisine": random.choice(cuisines),
                "caloriesPerServing": random.randint(
                    150,
                    700
                ),
                "tags": json.dumps(
                    [
                        "RetailHouse",
                        "CDC"
                    ]
                ),
                "userId": int(
                    users_df.sample(1)["id"].iloc[0]
                ),
                "image": f"https://retailhouse.local/recipes/{recipe_id}.jpg",
                "rating": round(
                    random.uniform(4.0, 5.0),
                    1
                ),
                "reviewCount": random.randint(
                    0,
                    100
                ),
                "mealType": json.dumps(
                    [
                        random.choice(meal_types)
                    ]
                ),
                "batch_id": batch_id,
                "ingestion_timestamp": ingestion_timestamp,
                "source_system": "cdc_simulator"
            }
        )

    result_df = pd.DataFrame(rows)

    result_df.to_sql(
        "recipes",
        con=engine,
        schema="raw",
        if_exists="append",
        index=False
    )

    print(
        f"{len(result_df)} recipes inserted"
    )


if __name__ == "__main__":
    simulate_recipes_cdc()