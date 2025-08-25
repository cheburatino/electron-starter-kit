import uuid
from datetime import datetime, timezone, timedelta
from infra.abc.infra_element import InfraElement
from infra.tool.jwt_manager.jwt_manager import JwtManager
from .config import UserTokenManagerConfig


class UserTokenManager(InfraElement):
    def __init__(self, config: UserTokenManagerConfig, jwt_manager: JwtManager):
        if config is None:
            raise ValueError("config не может быть None")
        if jwt_manager is None:
            raise ValueError("jwt_manager не может быть None")
            
        self._config = config
        self._jwt_manager = jwt_manager

    async def create_access_token(self, user_id: int) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "expires_at": int((now + timedelta(minutes=self._config.access_token_expire_minutes)).timestamp()),
            "created_at": int(now.timestamp())
        }
        
        return await self._jwt_manager.encode_token(payload)
    
    async def decode_access_token(self, token: str) -> dict | None:
        return await self._jwt_manager.decode_token(token)
    
    async def verify_access_token(self, token: str) -> bool:
        try:
            payload = await self._jwt_manager.decode_token(token)
            if not payload:
                return False
            
            expires_at = payload.get("expires_at")
            if not expires_at:
                return False
                
            return datetime.now(timezone.utc).timestamp() < expires_at
        except Exception:
            return False

    def create_refresh_token(self) -> tuple[str, datetime]:
        refresh_token = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(days=self._config.refresh_token_expire_days)
        return refresh_token, expires_at


def get_user_token_manager() -> UserTokenManager:
    return UserTokenManager.get_from_container("user_token_manager")
