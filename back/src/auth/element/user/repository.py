from infra.tool.postgres_client.postgres_client import PostgresClient
from repository.postgres.table_crud import TableCrud


class UserRepository(TableCrud):
    def __init__(self, db_client: PostgresClient, table_name: str = '"user"'):
        super().__init__(db_client, table_name)
    
    async def get_by_auth_email(self, auth_email: str, tx=None) -> dict | None:
        filters = [{"field": "auth_email", "value": auth_email, "operator": "="}]
        results = await self.get_list(filters=filters, page_count=1, page_number=1, tx=tx)
        return results[0] if results else None
    
    async def get_active_users(self, tx=None) -> list[dict]:
        filters = [{"field": "has_access", "value": True, "operator": "="}]
        return await self.get_list(filters=filters, page_count=100, page_number=1, tx=tx)
    