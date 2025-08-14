from core.settings.settings import Settings, get_settings
from tool.jwt_manager.tool import get_manager, JwtManager
from adapter.pyjwt_client.adapter import get_client
from adapter.abc.jwt_client.settings import Settings as JwtClientSettings


def _get_jwt_manager() -> JwtManager:
    settings: Settings = get_settings()
    jwt_client_settings: JwtClientSettings = settings.get_jwt_client_settings()
    
    jwt_client = get_client(settings=jwt_client_settings)
    return get_manager(jwt_client=jwt_client)


def start_jwt_manager() -> JwtManager:
    print("Инициализация JWT Manager...")
    try:
        jwt_manager = _get_jwt_manager()
        print("JWT Manager успешно инициализирован")
        return jwt_manager
            
    except Exception as e:
        print(f"Критическая ошибка при инициализации JWT Manager: {e}")
        raise 