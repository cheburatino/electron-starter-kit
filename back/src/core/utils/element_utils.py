from abc import ABC, abstractmethod
from core.utils.object_utils import ObjectUtils
from back.src.infra.tool.postgres_client.postgres_client import PostgresClient
from state.live.object_container.models import ObjectKey


class ElementUtils(ObjectUtils, ABC):
    @classmethod
    @abstractmethod
    def _create_repository(cls, db_client):
        pass
    
    @classmethod
    @abstractmethod
    def _extract_id(cls, data: dict):
        pass

    @classmethod
    async def create(cls, db_client: PostgresClient, ttl_seconds: int = 3600, **data):
        async with db_client.transaction_manager.transaction():
            repository = cls._create_repository(db_client)
            result = await repository.create(data)
            id = cls._extract_id(result)

            return super().factory(str(id), ttl_seconds, 
                                 db_client=db_client, id=id, data=result)
    
    @classmethod
    async def get(cls, obj_id: str, db_client: PostgresClient, ttl_seconds: int = 3600):
        cached = cls._get_from_object_container(obj_id)
        if cached:
            return cached
        
        async with db_client.transaction_manager.transaction():
            repository = cls._create_repository(db_client)
            data = await repository.get_by_id(int(obj_id))
            
            if not data:
                return None
            
            id = cls._extract_id(data)
            return super().factory(str(id), ttl_seconds,
                                 db_client=db_client, id=id, data=data)
    
    @classmethod
    def _get_from_object_container(cls, obj_id: str):
        category = cls._get_object_path()
        container = cls._get_container()
        key = ObjectKey(category=category, obj_id=obj_id)
        try:
            return container.storage.get_entry(key).instance
        except:
            return None
    
    @classmethod
    def _remove_from_object_container(cls, obj_id: str):
        category = cls._get_object_path()
        container = cls._get_container()
        key = ObjectKey(category=category, obj_id=obj_id)
        try:
            return container.storage.remove_entry(key)
        except:
            return False
    
    @classmethod
    async def list(cls, db_client: PostgresClient, filters: dict = None, ttl_seconds: int = 3600):
        async with db_client.transaction_manager.transaction():
            repository = cls._create_repository(db_client)
            data_list = await repository.list(filters)
            
            instances = []
            for data in data_list:
                id = cls._extract_id(data)
                obj_id = str(id)
                
                cached = cls._get_from_object_container(obj_id)
                if cached:
                    instances.append(cached)
                else:
                    instance = super().factory(obj_id, ttl_seconds,
                                             db_client=db_client, id=id, data=data)
                    instances.append(instance)
            
            return instances
