from abc import ABC, abstractmethod
import uuid
from core.utils.object_utils import ObjectUtils


class ScenarioUtils(ObjectUtils):
    @classmethod
    def create(cls, ttl_seconds: int = 3600, **kwargs) -> object:
        obj_id = str(uuid.uuid4())
        return super().factory(obj_id, ttl_seconds, **kwargs)