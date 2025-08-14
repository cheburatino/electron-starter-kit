from abc import ABC, abstractmethod
from infra.tool.postgres_client.postgres_client import PostgresClient


class Repository(ABC):
    client: PostgresClient
    
    @abstractmethod
    async def create(self, data: dict, res_columns: list = None) -> dict | None:
        pass
    
    @abstractmethod
    async def get_by_id(self, id_value: int, res_columns: list = None) -> dict | None:
        pass
    
    @abstractmethod
    async def get_list(self, filters: list = None, include_deleted: bool = False, res_columns: list = None, orderby: dict = None, page_count: int = None, page_number: int = None) -> list[dict]:
        pass
    
    @abstractmethod
    async def update(self, id_value: int, data: dict, res_columns: list = None) -> dict | None:
        pass
    
    @abstractmethod
    async def soft_delete(self, id_value: int, res_columns: list = None) -> dict | None:
        pass

    @abstractmethod
    async def hard_delete(self, id_value: int, res_columns: list = None) -> dict | None:
        pass
    
    @abstractmethod
    async def get_id_by_code(self, code: str) -> int | None:
        pass