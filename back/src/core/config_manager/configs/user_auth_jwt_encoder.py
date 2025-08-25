import os
from infra.adapter.jwt_encoder_py_jwt.config import JwtEncoderPyJwtConfig


def _from_env() -> JwtEncoderPyJwtConfig:
    secret_key = os.environ.get("USER_AUTH_JWT_SECRET_KEY")
    algorithm_type = os.environ.get("USER_AUTH_JWT_ALGORITHM_TYPE")
    
    if not all([secret_key, algorithm_type]):
        raise ValueError("Не указаны необходимые параметры для JWT encoder (USER_AUTH_JWT_SECRET_KEY, USER_AUTH_JWT_ALGORITHM_TYPE)")
    
    return JwtEncoderPyJwtConfig(
        secret_key=secret_key,
        algorithm_type=algorithm_type
    )

def get_user_auth_jwt_encoder_config() -> JwtEncoderPyJwtConfig:
    return _from_env()