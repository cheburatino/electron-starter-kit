from abc import ABC, abstractmethod
from infra.system.postgresql.system import PostgresConnectionConfig


class Connector(ABC):
    @abstractmethod
    def __init__(self, connection_config: PostgresConnectionConfig):
        pass

    @property
    @abstractmethod
    def pool(self):
        pass

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass