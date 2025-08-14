from infra.abc.infra_element import InfraElement
from infra.system.postgresql.system import PostgresConnectionConfig
from infra.adapter.abc.postgres_client.adapter import PostgresClient as AbstractPostgresClient
from .connector import Connector
from .executor import Executor
from .transaction_manager import TransactionManager


class PostgresClientAsyncpg(InfraElement, AbstractPostgresClient):
    Connector = Connector
    Executor = Executor
    TransactionManager = TransactionManager
    
    def __init__(self, connection_config: PostgresConnectionConfig):
        if connection_config is None:
            raise ValueError("connection_config не может быть None")
        self._connection_config = connection_config
        self._connector = self.Connector(connection_config)
        self._executor = self.Executor()
        self._transaction_manager = self.TransactionManager(connector=self._connector)

    @property
    def connector(self) -> Connector:
        return self._connector

    @property
    def executor(self) -> Executor:
        return self._executor

    @property
    def transaction_manager(self) -> TransactionManager:
        return self._transaction_manager

    @property
    def connection_config(self) -> PostgresConnectionConfig:
        return self._connection_config


def get_main_db_adapter() -> PostgresClientAsyncpg:
    return PostgresClientAsyncpg.get_from_container("main_db_adapter")


def get_analytic_db_adapter() -> PostgresClientAsyncpg:
    return PostgresClientAsyncpg.get_from_container("analytic_db_adapter")
