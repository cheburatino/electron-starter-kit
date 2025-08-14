from datetime import datetime

from infra.tool.postgres_client.postgres_client import PostgresClient
from .table_crud import TableCrud
from .repository import Repository


class RepositoryMixin:
    _repository_class: Repository | None = None
    _db_table_name: str = None
    _default_repository_class: Repository = TableCrud

    _cached_db_client: PostgresClient = None
    _cached_repository: Repository = None

    id: int = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    @property
    def db_client(self) -> PostgresClient:
        return self._db_client

    @property
    def repository(self) -> Repository:
        return self._repository


    @classmethod
    def _get_db_client(cls) -> PostgresClient:
        if cls._cached_db_client is None:
            cls._cached_db_client = PostgresClient.get_from_container("main_db")
        return cls._cached_db_client

    @classmethod
    def _get_repository(cls) -> Repository:
        if cls._cached_repository is None:
            client = cls._get_db_client()
            if cls._repository_class is not None:
                cls._cached_repository = cls._repository_class(client)
            elif cls._db_table_name is not None:
                cls._cached_repository = cls._default_repository_class(client, cls._db_table_name)
            else:
                raise ValueError(
                    f"{cls.__name__} must define _repository_class or _db_table_name"
                )
        return cls._cached_repository

    @classmethod
    def _instantiate(cls, el_id: str, db_client: PostgresClient, repository: Repository):
        return cls(el_id, db_client, repository)

    def _populate_from_data(self, data: dict):
        annotations = {}
        for cls in self.__class__.__mro__:
            class_annotations = getattr(cls, "__annotations__", {})
            annotations.update(class_annotations)

        for field_name, field_type in annotations.items():
            if field_name.startswith("_"):
                continue
            if field_name in data:
                value = data[field_name]
                setattr(self, field_name, value)


    @classmethod
    async def create(cls, data: dict, db_client: PostgresClient = None, repository: Repository = None):
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()

        async with actual_db_client.transaction_manager.transaction():
            result = await actual_repository.create(data)

            instance = cls._instantiate(str(result["id"]), actual_db_client, actual_repository)
            instance.id = result["id"]
            instance._populate_from_data(result)
            return instance

    @classmethod
    async def get_by_id(
        cls,
        id_value: int,
        db_client: PostgresClient = None,
        repository: Repository = None,
    ):
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()

        async with actual_db_client.transaction_manager.transaction():
            data = await actual_repository.get_by_id(id_value)
            if data:
                instance = cls._instantiate(str(data["id"]), actual_db_client, actual_repository)
                instance._populate_from_data(data)
                return instance
            return None

    @classmethod
    async def get_list(
        cls,
        filters: list = None,
        include_deleted: bool = False,
        db_client: PostgresClient = None,
        repository: Repository = None,
        **kwargs,
    ):
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()

        async with actual_db_client.transaction_manager.transaction():
            result = await actual_repository.get_list(filters, include_deleted, **kwargs)
            instances = []
            for data in result:
                instance = cls._instantiate(str(data["id"]), actual_db_client, actual_repository)
                instance._populate_from_data(data)
                instances.append(instance)
            return instances

    @classmethod
    async def update_by_id(
        cls,
        id_value: int,
        data: dict,
        db_client: PostgresClient = None,
        repository: Repository = None,
    ):
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()

        async with actual_db_client.transaction_manager.transaction():
            result = await actual_repository.update(id_value, data)
            if result:
                instance = cls._instantiate(str(result["id"]), actual_db_client, actual_repository)
                instance._populate_from_data(result)
                return instance
            return None

    @classmethod
    async def soft_delete_by_id(
        cls,
        id_value: int,
        db_client: PostgresClient = None,
        repository: Repository = None,
    ):
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()

        async with actual_db_client.transaction_manager.transaction():
            result = await actual_repository.soft_delete(id_value)
            if result:
                instance = cls._instantiate(str(result["id"]), actual_db_client, actual_repository)
                instance._populate_from_data(result)
                return instance
            return None

    @classmethod
    async def hard_delete_by_id(
        cls,
        id_value: int,
        db_client: PostgresClient = None,
        repository: Repository = None,
    ):
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()

        async with actual_db_client.transaction_manager.transaction():
            result = await actual_repository.hard_delete(id_value)
            if result:
                instance = cls._instantiate(str(result["id"]), actual_db_client, actual_repository)
                instance._populate_from_data(result)
                return instance
            return None

    @classmethod
    async def get_id_by_code(
        cls,
        code: str,
        db_client: PostgresClient = None,
        repository: Repository = None,
    ) -> int | None:
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()

        async with actual_db_client.transaction_manager.transaction():
            return await actual_repository.get_id_by_code(code)


    async def refresh(self):
        if not self.id:
            raise ValueError("Cannot refresh element without ID")

        async with self.db_client.transaction_manager.transaction():
            data = await self.repository.get_by_id(self.id)
            if data:
                self._populate_from_data(data)
            return data

    async def update(self, **data):
        if not self.id:
            raise ValueError("Cannot update element without ID")

        async with self.db_client.transaction_manager.transaction():
            result = await self.repository.update(self.id, data)
            if result:
                self._populate_from_data(result)
            return result

    async def delete(self):
        if not self.id:
            raise ValueError("Cannot delete element without ID")

        async with self.db_client.transaction_manager.transaction():
            return await self.repository.soft_delete(self.id)

    async def hard_delete(self):
        if not self.id:
            raise ValueError("Cannot delete element without ID")
        async with self.db_client.transaction_manager.transaction():
            return await self.repository.hard_delete(self.id)