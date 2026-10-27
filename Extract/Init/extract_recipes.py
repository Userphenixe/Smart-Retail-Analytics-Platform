from Extract.load_api_to_postgres import load_api_to_postgres

load_api_to_postgres(
    endpoint="recipes",
    root_key="recipes",
    table_name="recipes",
)