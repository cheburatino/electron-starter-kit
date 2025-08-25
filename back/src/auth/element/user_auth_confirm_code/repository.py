from infra.tool.postgres_client.postgres_client import PostgresClient
from repository.postgres.table_crud import TableCrud
from infra.tool.postgres_client.query_executor import Query


class UserAuthConfirmCodeRepository(TableCrud):
    def __init__(self, db_client: PostgresClient, table_name: str = "user_auth_confirm_code"):
        super().__init__(db_client, table_name)
        
    async def get_by_token(self, token: str, tx=None) -> dict | None:
        sql = f"SELECT * FROM {self.table_name} WHERE token = $1 AND deleted_at IS NULL"
        query = Query(sql, [token], fetch=True)
        result = await self.client.query_executor.execute_query(query, tx=tx)
        
        if len(result) > 1:
            raise ValueError(f"Найдено {len(result)} записей с token='{token}'. Ожидалось: 0 или 1")
        
        return result[0] if result else None
