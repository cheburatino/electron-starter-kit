from .kit.kit import Kit
from abc import ABC
from .kit.default_kits import get_default_kit


class StateMixin(ABC):
    el_id: str
    category: str
    kit: Kit
        
    def __init_subclass__(cls, kit: Kit | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        
        cls.category = cls.__module__
        
        if kit is None:
            cls.kit = get_default_kit(cls)
        else:
            cls.kit = kit
    
    @classmethod
    def get_from_container(cls, el_id: str):
        existing = cls.kit.object_container_manager.get(el_id)
        if not existing:
            raise ValueError(f"{cls.__name__} with id '{el_id}' not found in container")
        return existing
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(el_id={self.el_id})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(el_id='{self.el_id}', category='{self.category}')"
    