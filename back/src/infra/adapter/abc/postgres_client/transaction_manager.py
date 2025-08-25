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
    async def tx_context_manager(self) -> AsyncIterator:
        yield None

    @abstractmethod
    async def begin(self):
        pass 