from Extract.load_api_to_postgres import load_api_to_postgres

load_api_to_postgres(
    endpoint="users",
    root_key="users",
    table_name="users",)