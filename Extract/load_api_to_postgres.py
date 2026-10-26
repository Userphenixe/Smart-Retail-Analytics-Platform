import json
import requests
import pandas as pd
import urllib3

from datetime import datetime
from sqlalchemy import create_engine

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

engine = create_engine(
    "postgresql+psycopg2://admin:admin@postgres:5432/analytics"
)


def load_api_to_postgres(
    endpoint: str,
    root_key: str,
    table_name: str,
    schema: str = "raw"
):
    url = f"https://dummyjson.com/{endpoint}"

    response = requests.get(
        url,
        verify=False
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(data[root_key])


    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: json.dumps(x)
            if isinstance(x, (dict, list))
            else x
        )

    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")

    df["batch_id"] = batch_id
    df["ingestion_timestamp"] = datetime.now()
    df["source_system"] = "dummyjson"

    df.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False
    )

    print(
        f"{len(df)} rows loaded into {schema}.{table_name}"
    )