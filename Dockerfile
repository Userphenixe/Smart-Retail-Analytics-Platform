FROM apache/airflow:2.10.5

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    requests

# RUN python -m pip install \
#     --trusted-host pypi.org \
#     --trusted-host files.pythonhosted.org \
#     dbt-postgres==1.11.0