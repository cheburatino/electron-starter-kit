import os
from infra.system.postgresql.postgresql import PostgresConnectionConfig


def _from_env() -> PostgresConnectionConfig:
    host = os.environ.get("MAIN_DB_HOST")
    port = int(os.environ.get("MAIN_DB_PORT"))
    database_name = os.environ.get("MAIN_DB_NAME")
    user = os.environ.get("MAIN_DB_USER")
    password = os.environ.get("MAIN_DB_PASSWORD")
    pool_min_size = int(os.environ.get("MAIN_DB_POOL_MIN_SIZE"))
    pool_max_size = int(os.environ.get("MAIN_DB_POOL_MAX_SIZE"))
    
    return PostgresConnectionConfig(
        host=host,
        port=port,
        name=database_name,
        user=user,
        password=password,
        pool_min_size=pool_min_size,
        pool_max_size=pool_max_size
    )

def get_main_db_config() -> PostgresConnectionConfig:
    return _from_env()