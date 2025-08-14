from datetime import datetime, timedelta, timezone
import jwt
from functools import lru_cache

from adapter.abc.jwt_client.adapter import JwtClient
from adapter.abc.jwt_client.settings import Settings as JwtClientSettings


class PyJwtClient(JwtClient):
    def __init__(self, settings: JwtClientSettings):
        self._settings = settings

    async def encode_token(self, payload: dict, expires_delta_minutes: int) -> str:
        payload_to_encode = payload.copy()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_delta_minutes)
        payload_to_encode.update({
            "expires_at": expires_at,
            "created_at": datetime.now(timezone.utc)
        })
        
        encoded_jwt = jwt.encode(
            payload_to_encode,
            self._settings.secret_key,
            algorithm=self._settings.algorithm_type
        )
        return encoded_jwt

    async def decode_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                self._settings.secret_key,
                algorithms=[self._settings.algorithm_type]
            )
            return payload
        except jwt.PyJWTError as e:
            print(f"JWT decoding/validation failed: {e}")  # Замените на логгирование
            return None

    async def verify_token(self, token: str) -> bool:
        payload = await self.decode_token(token)
        return payload is not None

    @property
    def settings(self) -> JwtClientSettings:
        return self._settings


@lru_cache(maxsize=1)
def get_client(settings: JwtClientSettings) -> PyJwtClient:
    return PyJwtClient(settings=settings) 