from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from .connector import Connector


class TransactionManager(ABC):
    @abstractmethod
    def __init__(self, connector: Connector):
        pass

    @abstractmethod
    @asynccontextmanager
    async def begin_transaction(self) -> AsyncIterator:
        yield None 