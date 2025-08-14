from datetime import datetime, UTC

from infra.tool.postgres_client.postgres_client import PostgresClient
from repository.postgres.table_crud import TableCrud


class UserAuthConfirmCodeRepository(TableCrud):
    def __init__(self, db_client: PostgresClient, table_name: str = "user_auth"):
        super().__init__(db_client, table_name)
