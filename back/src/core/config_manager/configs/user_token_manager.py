import os
from infra.tool.user_token_manager.config import UserTokenManagerConfig


def _from_env() -> UserTokenManagerConfig:
    access_token_expire_minutes = int(os.environ.get("USER_AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"))
    refresh_token_expire_days = int(os.environ.get("USER_AUTH_REFRESH_TOKEN_EXPIRE_DAYS"))
    
    return UserTokenManagerConfig(
        access_token_expire_minutes=access_token_expire_minutes,
        refresh_token_expire_days=refresh_token_expire_days
    )

def get_user_token_manager_config() -> UserTokenManagerConfig:
    return _from_env()
