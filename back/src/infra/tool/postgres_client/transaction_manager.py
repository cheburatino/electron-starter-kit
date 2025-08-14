from contextlib import asynccontextmanager

from infra.adapter.abc.postgres_client.adapter import PostgresClient
from .query_executor import QueryExecutor


class TransactionManager:
    def __init__(self, client_adapter: PostgresClient, main_client=None):
        if client_adapter is None:
            raise ValueError("Адаптер клиента (client_adapter) не может быть None")
        self._client_adapter = client_adapter
        self._main_client = main_client

    @asynccontextmanager
    async def transaction(self):
        async with self._client_adapter.transaction_manager.begin_transaction() as conn:
            tx_executor = QueryExecutor(self._client_adapter)
            tx_executor._conn = conn
            
            # Временно подменяем query_executor на транзакционный
            original_executor = None
            try:
                if self._main_client:
                    original_executor = self._main_client._query_executor
                    self._main_client._query_executor = tx_executor
                
                yield tx_executor
            finally:
                # Восстанавливаем оригинальный executor
                if self._main_client and original_executor:
                    self._main_client._query_executor = original_executor
