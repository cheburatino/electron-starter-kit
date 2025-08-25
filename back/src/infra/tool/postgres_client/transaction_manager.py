from contextlib import asynccontextmanager

from infra.adapter.abc.postgres_client.adapter import PostgresClient


class Transaction:
    def __init__(self, connection):
        self.connection = connection


class ManualTransaction:
    def __init__(self, low_level_tx):
        self._low_level_tx = low_level_tx
        self.connection = low_level_tx.connection
        self._completed = False

    async def commit(self):
        if self._completed:
            raise RuntimeError("Транзакция уже завершена")
        
        await self._low_level_tx.commit()
        self._completed = True

    async def rollback(self):
        if self._completed:
            raise RuntimeError("Транзакция уже завершена")
        
        await self._low_level_tx.rollback()
        self._completed = True

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._completed:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()


class TransactionManager:
    def __init__(self, client_adapter: PostgresClient):
        if client_adapter is None:
            raise ValueError("Адаптер клиента (client_adapter) не может быть None")
        self._client_adapter = client_adapter

    @asynccontextmanager
    async def transaction(self):
        """Контекстный менеджер для транзакций - возвращает простой объект с соединением"""
        async with self._client_adapter.transaction_manager.tx_context_manager() as conn:
            yield Transaction(conn)

    async def begin(self) -> ManualTransaction:
        """Ручное управление транзакциями"""
        low_level_tx = await self._client_adapter.transaction_manager.begin()
        return ManualTransaction(low_level_tx)
