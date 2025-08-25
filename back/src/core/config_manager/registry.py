from .configs.main_db import get_main_db_config
from .configs.main_tg_bot import get_main_tg_bot_config
from .configs.main_email import get_main_email_config
from .configs.user_auth_jwt_encoder import get_user_auth_jwt_encoder_config
from .configs.user_token_manager import get_user_token_manager_config


class Registry:
    def __init__(self):
        self._registry = {
            'main_db': get_main_db_config,
            'main_tg_bot': get_main_tg_bot_config,
            'main_email': get_main_email_config,
            'user_auth_jwt_encoder': get_user_auth_jwt_encoder_config,
            'user_token_manager': get_user_token_manager_config,
        }
    
    def get_config(self, key: str):
        if key not in self._registry:
            available_keys = ', '.join(self._registry.keys())
            raise ValueError(f"Config '{key}' not found. Available configs: {available_keys}")
        return self._registry[key]()
