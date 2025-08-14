import sys
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from infra.adapter.abc.postgres_client.transaction_manager import TransactionManager as AbstractTransactionManager
from infra.adapter.abc.postgres_client.connector import Connector


class TransactionManager(AbstractTransactionManager):
    def __init__(self, connector: Connector):
        if connector is None:
            raise ValueError("Connector не может быть None для TransactionManager")
        self._connector = connector

    @asynccontextmanager
    async def begin_transaction(self) -> AsyncIterator:
        if self._connector.pool is None:
            raise RuntimeError("Пул соединений не инициализирован перед началом транзакции.")
        
        conn = None
        tx_context = None
        pool = self._connector.pool

        try:
            conn = await pool.acquire()
            tx_context = conn.transaction()
            await tx_context.__aenter__()
            yield conn
        except Exception:
            raise
        finally:
            if conn and tx_context:
                exc_info = sys.exc_info()
                await tx_context.__aexit__(*exc_info)
            if conn:
                await pool.release(conn) 