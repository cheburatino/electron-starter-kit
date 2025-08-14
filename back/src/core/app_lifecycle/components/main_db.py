from core.config_manager.config_manager import ConfigManager, Utils as ConfigManagerUtils
from infra.tool.postgres_client.postgres_client import PostgresClient
from infra.adapter.postgres_client_asyncpg.postgres_client_asyncpg import PostgresClientAsyncpg
from infra.system.postgresql.system import PostgresConnectionConfig


def _create_main_db_client() -> PostgresClient:
    config_manager: ConfigManager = ConfigManagerUtils.get("config_manager")
    
    connection_config: PostgresConnectionConfig = config_manager.registry.get_config('main_db')
    
    adapter = PostgresClientAsyncpg(el_id="main_db_adapter", connection_config=connection_config)
    main_db_client = PostgresClient(el_id="main_db", client_adapter=adapter)
    
    return main_db_client


async def connect_main_db():
    main_db_client: PostgresClient = _create_main_db_client()
    await main_db_client.connector.connect()
    await main_db_client.connector.health_check()
    print("Main database connected successfully")


async def disconnect_main_db():
    main_db_client: PostgresClient = PostgresClient.get_from_container("main_db")
    await main_db_client.connector.disconnect()
    print("Main database disconnected")