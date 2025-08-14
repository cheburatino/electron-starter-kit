from infra.adapter.abc.postgres_client.adapter import PostgresClient


class Connector:
    def __init__(self, client_adapter: PostgresClient):
        if client_adapter is None:
            raise ValueError("Адаптер клиента (client_adapter) не может быть None")
        self._client_adapter = client_adapter

    async def connect(self) -> None:
        await self._client_adapter.connector.connect()

    async def disconnect(self) -> None:
        await self._client_adapter.connector.disconnect()

    async def health_check(self) -> bool:
        return await self._client_adapter.connector.health_check()

    @property
    def client_adapter(self) -> PostgresClient:
        return self._client_adapter