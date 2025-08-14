from functools import lru_cache
from adapter.abc.jwt_client.adapter import JwtClient


class JwtManager:
    def __init__(self, jwt_client: JwtClient):
        self._jwt_client = jwt_client

    async def create_access_token(self, payload: dict) -> str:
        return await self._jwt_client.encode_token(
            payload=payload,
            expires_delta_minutes=self._jwt_client.settings.access_token_expire_minutes
        )

    async def create_refresh_token(self, payload: dict) -> str:
        expires_delta_minutes = self._jwt_client.settings.refresh_token_expire_days * 24 * 60
        return await self._jwt_client.encode_token(
            payload=payload,
            expires_delta_minutes=expires_delta_minutes
        )

    async def verify_token(self, token: str) -> bool:
        return await self._jwt_client.verify_token(token)

    async def decode_token(self, token: str) -> dict | None:
        return await self._jwt_client.decode_token(token)


@lru_cache(maxsize=10)
def get_manager(jwt_client: JwtClient) -> JwtManager:
    return JwtManager(jwt_client=jwt_client)