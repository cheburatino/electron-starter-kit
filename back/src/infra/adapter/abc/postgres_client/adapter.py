from abc import ABC, abstractmethod

from infra.system.postgresql.postgresql import PostgresConnectionConfig
from .connector import Connector
from .executor import Executor
from .transaction_manager import TransactionManager


class PostgresClient(ABC):
    Connector = Connector
    Executor = Executor
    TransactionManager = TransactionManager

    @abstractmethod
    def __init__(self, connection_config: PostgresConnectionConfig):
        pass

    @property
    def connection_config(self) -> PostgresConnectionConfig:
        return self.connection_config

    @property
    @abstractmethod
    def connector(self) -> Connector:
        pass

    @property
    @abstractmethod
    def executor(self) -> Executor:
        pass

    @property
    @abstractmethod
    def transaction_manager(self) -> TransactionManager:
        pass
