from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore

with DAG(
    dag_id="retailhouse",
    start_date=datetime(2026, 1, 26),
    schedule="0 */6 * * *",
    catchup=False,
    tags=["retailhouse"],
) as dag:

    generate_products = BashOperator(
        task_id="generate_products",
        bash_command="""
        python /opt/airflow/extract/cdc_products.py
        """
    )