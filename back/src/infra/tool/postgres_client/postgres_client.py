from infra.abc.infra_element import InfraElement
from infra.system.postgresql.postgresql import PostgresConnectionConfig
from infra.adapter.abc.postgres_client.adapter import PostgresClient as AbstractPostgresClientAdapter

from .connector import Connector
from .query_executor import QueryExecutor
from .transaction_manager import TransactionManager


class PostgresClient(InfraElement):
    Connector = Connector
    TransactionManager = TransactionManager
    QueryExecutor = QueryExecutor
    
    def __init__(self, client_adapter: AbstractPostgresClientAdapter):
        if client_adapter is None:
            raise ValueError("client_adapter не может быть None")
        self._client_adapter = client_adapter
        self._connector = self.Connector(self._client_adapter)
        self._transaction_manager = self.TransactionManager(self._client_adapter)
        self._query_executor = self.QueryExecutor(self._client_adapter)

    @property
    def connection_config(self) -> PostgresConnectionConfig:
        return self.client_adapter.connection_config

    @property
    def client_adapter(self):
        return self._client_adapter

    @property
    def connector(self) -> Connector:
        return self._connector

    @property
    def query_executor(self) -> QueryExecutor:
        return self._query_executor

    @property
    def transaction_manager(self) -> TransactionManager:
        return self._transaction_manager

    async def health_check(self) -> bool:
        return await self.connector.health_check()

def get_main_db() -> PostgresClient:
    return PostgresClient.get_from_container("main_db")


def get_analytic_db() -> PostgresClient:
    return PostgresClient.get_from_container("analytic_db")
