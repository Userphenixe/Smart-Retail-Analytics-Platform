from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore

import sys

sys.path.append("/opt/airflow/extract")

from cdc_products import simulate_products_cdc # type: ignore
from cdc_users import simulate_users_cdc # type: ignore
from cdc_carts import simulate_carts_cdc # type: ignore


with DAG(
    dag_id="retailhouse",

    start_date=datetime(2026, 1, 26),

    schedule="0 */6 * * *",

    catchup=False,

    tags=["retailhouse", "cdc", "simulation"],

) as dag:

    generate_products = PythonOperator(

        task_id="generate_products",

        python_callable=simulate_products_cdc

    )

    generate_users = PythonOperator(

        task_id="generate_users",

        python_callable=simulate_users_cdc

    )

    generate_carts = PythonOperator(

        task_id="generate_carts",

        python_callable=simulate_carts_cdc

    )