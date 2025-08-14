import os
from infra.adapter.abc.jwt_client.settings import Settings as JwtClientSettings


def _from_env() -> JwtClientSettings:
    secret_key = os.environ.get("JWT_SECRET_KEY")
    algorithm_type = os.environ.get("JWT_ALGORITHM_TYPE")
    access_token_expire_minutes = os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days = os.environ.get("JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    if not all([secret_key, algorithm_type, access_token_expire_minutes, refresh_token_expire_days]):
        raise ValueError("Не указаны необходимые параметры для JWT клиента (JWT_SECRET_KEY, JWT_ALGORITHM_TYPE, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_TOKEN_EXPIRE_DAYS)")
    
    return JwtClientSettings(
        secret_key=secret_key,
        algorithm_type=algorithm_type,
        access_token_expire_minutes=int(access_token_expire_minutes),
        refresh_token_expire_days=int(refresh_token_expire_days)
    )

def get_jwt_client_config() -> JwtClientSettings:
    return _from_env()