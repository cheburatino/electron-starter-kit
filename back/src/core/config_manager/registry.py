from .configs.main_db import get_main_db_config
from .configs.main_tg_bot import get_main_tg_bot_config
from .configs.main_email import get_main_email_config
from .configs.jwt_client import get_jwt_client_config


class Registry:
    def __init__(self):
        self._registry = {
            'main_db': get_main_db_config,
            'main_tg_bot': get_main_tg_bot_config,
            'main_email': get_main_email_config,
            'jwt_client': get_jwt_client_config,
        }
    
    def get_config(self, key: str):
        if key not in self._registry:
            available_keys = ', '.join(self._registry.keys())
            raise ValueError(f"Config '{key}' not found. Available configs: {available_keys}")
        return self._registry[key]()