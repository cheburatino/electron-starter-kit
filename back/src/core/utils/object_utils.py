from abc import ABC, abstractmethod
from state.live.object_container.object_container import ObjectContainer
from state.live.object_container.models import ObjectKey, ObjectEntry, ObjectMetadata


class ObjectUtils(ABC):
    _path_cache: dict[type, str] = {}
    
    @classmethod
    def _get_object_path(cls) -> str:
        if cls not in cls._path_cache:
            cls._path_cache[cls] = cls._parse_module_path()
        return cls._path_cache[cls]
    
    @classmethod
    def _parse_module_path(cls) -> str:
        module = cls.__module__
        return module
    
    @classmethod
    def _get_container(cls) -> ObjectContainer:
        return ObjectContainer.get_instance()
    
    @classmethod
    def get(cls, obj_id: str) -> object | None:
        category = cls._get_object_path()
        container = cls._get_container()
        key = ObjectKey(category=category, id=obj_id)
        entry = container.storage.get(key)
        return entry.instance if entry else None
    
    @classmethod
    @abstractmethod
    def _create(cls, **kwargs) -> object:
        pass
    
    @classmethod
    def _save(cls, obj_id: str, instance: object, ttl_seconds: int = 3600):
        category = cls._get_object_path()
        container = cls._get_container()
        key = ObjectKey(category=category, id=obj_id)
        metadata = ObjectMetadata(ttl_seconds=ttl_seconds)
        entry = ObjectEntry(instance=instance, metadata=metadata)
        container.storage.add(key, entry)
    
    @classmethod
    def factory(cls, obj_id: str, ttl_seconds: int, **kwargs) -> object:
        instance = cls._create(**kwargs)
        cls._save(obj_id, instance, ttl_seconds)
        return instance
