from core.config_manager.config_manager import ConfigManager, Utils as ConfigManagerUtils
from infra.tool.user_token_manager.config import UserTokenManagerConfig
from infra.tool.user_token_manager.user_token_manager import UserTokenManager
from infra.tool.jwt_manager.jwt_manager import JwtManager
from infra.adapter.jwt_encoder_py_jwt.jwt_encoder_py_jwt import JwtEncoderPyJwt
from infra.adapter.jwt_encoder_py_jwt.config import JwtEncoderPyJwtConfig


def _create_user_token_manager() -> UserTokenManager:
    config_manager: ConfigManager = ConfigManagerUtils.get("config_manager")
    
    encoder_config: JwtEncoderPyJwtConfig = config_manager.registry.get_config('user_auth_jwt_encoder')
    manager_config: UserTokenManagerConfig = config_manager.registry.get_config('user_token_manager')
    
    adapter = JwtEncoderPyJwt(el_id="user_auth_jwt_encoder", config=encoder_config)
    jwt_manager = JwtManager(el_id="user_auth_jwt_manager", jwt_encoder_adapter=adapter)
    
    user_token_manager = UserTokenManager(el_id="user_token_manager", config=manager_config, jwt_manager=jwt_manager)
    
    return user_token_manager


def start_user_token_manager() -> UserTokenManager:
    print("Инициализация User Token Manager...")
    try:
        user_token_manager = _create_user_token_manager()
        print("User Token Manager успешно инициализирован")
        return user_token_manager
            
    except Exception as e:
        print(f"Критическая ошибка при инициализации User Token Manager: {e}")
        raise
