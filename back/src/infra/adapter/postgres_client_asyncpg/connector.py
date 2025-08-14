import asyncpg
from infra.adapter.abc.postgres_client.connector import Connector as AbstractConnector
from infra.system.postgresql.system import PostgresConnectionConfig


class Connector(AbstractConnector):
    def __init__(self, connection_config: PostgresConnectionConfig):
        self.host = connection_config.host
        self.port = connection_config.port
        self.name = connection_config.name
        self.user = connection_config.user
        self.password = connection_config.password
        self.pool_min_size = connection_config.pool_min_size
        self.pool_max_size = connection_config.pool_max_size
        self._pool = None
    
    @property
    def pool(self):
        return self._pool

    async def connect(self) -> None:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.name,
                user=self.user,
                password=self.password,
                min_size=self.pool_min_size,
                max_size=self.pool_max_size
            )
            
            is_healthy = await self.health_check()
            if not is_healthy:
                await self.disconnect()
                raise RuntimeError("Проверка работоспособности соединения с БД не удалась после подключения")

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def health_check(self) -> bool:
        if self._pool is None:
            return False
        try:
            async with self._pool.acquire() as conn:
                await conn.fetchval('SELECT 1')
            return True
        except Exception:
            return False 