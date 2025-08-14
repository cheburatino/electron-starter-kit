from dataclasses import dataclass

from state.live.object_container.object_container import ObjectContainer
from state.live.object_container.models import ObjectEntry, ObjectMetadata, ObjectKey


@dataclass
class ObjectContainerManagerConfig:
    is_updatable: bool
    is_gettable: bool
    ttl_seconds: int
    
    def __post_init__(self):
        if self.ttl_seconds < -1:
            raise ValueError("TTL cannot be less than -1")


class ObjectContainerManager:
    def __init__(self, config: ObjectContainerManagerConfig, element_cls: type):
        self.config = config
        self.element_cls = element_cls
        self._container = ObjectContainer.get_instance()
    
    def add(self, obj, id: str):
        key = ObjectKey(
            category=self.element_cls.category,
            id=id
        )
        metadata = ObjectMetadata(ttl_seconds=self.config.ttl_seconds)
        entry = ObjectEntry(instance=obj, metadata=metadata)
        
        if self.config.is_updatable:
            self._container.storage.add_or_update(key, entry)
        else:
            self._container.storage.add(key, entry)
        
        return obj
    
    def get(self, id: str):
        if not self.config.is_gettable:
            raise ValueError("Getting objects from container is disabled for this element")
            
        key = ObjectKey(category=self.element_cls.category, id=id)
        entry = self._container.storage.get(key)
        
        if entry is None:
            return None
            
        return entry.instance
    
    def remove(self, id: str):
        key = ObjectKey(category=self.element_cls.category, id=id)
        return self._container.storage.remove(key)