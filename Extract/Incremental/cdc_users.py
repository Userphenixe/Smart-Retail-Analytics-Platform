import json
import random
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine


engine = create_engine(
    "postgresql+psycopg2://admin:admin@postgres:5432/analytics"
)


def simulate_users_cdc(nb_records=2):

    existing_users = pd.read_sql(
        """
        SELECT *
        FROM raw.users
        """,
        engine
    )

    max_id = existing_users["id"].max()

    first_names = [
        "Hamza", "Adam", "Lucas", "Sofia",
        "Emma", "Noah", "Lina", "Yasmine"
    ]

    last_names = [
        "Abbas", "Martin", "Bernard",
        "Smith", "Johnson", "Wilson"
    ]

    departments = [
        "Engineering",
        "Sales",
        "Marketing",
        "Finance",
        "Support"
    ]

    roles = [
        "user",
        "moderator"
    ]

    rows = []

    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")
    ingestion_timestamp = datetime.now()

    for i in range(nb_records):

        user_id = max_id + i + 1

        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        username = f"{first_name.lower()}{user_id}"

        rows.append(
            {
                "id": user_id,
                "firstName": first_name,
                "lastName": last_name,
                "maidenName": "",
                "age": random.randint(20, 60),
                "gender": random.choice(["male", "female"]),
                "email": f"{username}@retailhouse.com",
                "phone": f"+34 6{random.randint(10000000,99999999)}",
                "username": username,
                "password": "RetailHouse123!",

                "birthDate": f"{random.randint(1970,2004)}-{random.randint(1,12):02d}-15",

                "image": f"https://dummyjson.com/icon/{username}/128",

                "bloodGroup": random.choice(
                    ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
                ),

                "height": round(random.uniform(160, 195), 2),
                "weight": round(random.uniform(55, 100), 2),

                "eyeColor": random.choice(
                    ["Brown","Blue","Green","Hazel"]
                ),

                "hair": json.dumps({
                    "color": random.choice(
                        ["Black","Brown","Blonde","Red"]
                    ),
                    "type": random.choice(
                        ["Straight","Curly","Wavy"]
                    )
                }),

                "ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",

                "address": json.dumps({
                    "address": f"{random.randint(1,999)} Main Street",
                    "city": random.choice(
                        ["Madrid","Paris","Casablanca","London"]
                    ),
                    "country": "Spain"
                }),

                "macAddress": "AA:BB:CC:DD:EE:FF",

                "university": "RetailHouse University",

                "bank": json.dumps({
                    "currency": "EUR",
                    "cardType": "Visa"
                }),

                "company": json.dumps({
                    "department": random.choice(departments),
                    "name": "RetailHouse",
                    "title": "Business Analyst"
                }),

                "ein": f"{random.randint(100,999)}-{random.randint(100,999)}",

                "ssn": f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}",

                "userAgent": "RetailHouse CDC Simulator",

                "crypto": json.dumps({
                    "coin": "Bitcoin"
                }),

                "role": random.choice(roles),

                "batch_id": batch_id,
                "ingestion_timestamp": ingestion_timestamp,
                "source_system": "cdc_simulator"
            }
        )

    result_df = pd.DataFrame(rows)

    result_df.to_sql(
        "users",
        engine,
        schema="raw",
        if_exists="append",
        index=False
    )

    print(f"{len(result_df)} users inserted")


if __name__ == "__main__":
    simulate_users_cdc()