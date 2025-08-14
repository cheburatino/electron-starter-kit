from core.utils.object_utils import ObjectUtils
from .registry import Registry


class ConfigManager:
    ConfigRegistry = Registry
    
    def __init__(self):
        self._registry = Registry()
    
    @property
    def registry(self) -> ConfigRegistry:
        return self._registry


class Utils(ObjectUtils):
    @classmethod
    def _create(cls, **kwargs) -> ConfigManager:
        return ConfigManager()
