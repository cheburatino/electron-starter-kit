from abc import ABC, abstractmethod
from adapter.abc.jwt_client.settings import Settings as JwtClientSettings


class JwtClient(ABC):
    def __init__(self, settings: JwtClientSettings):
        pass

    @abstractmethod
    async def encode_token(self, payload: dict, expires_delta_minutes: int) -> str:
        pass

    @abstractmethod
    async def decode_token(self, token: str) -> dict | None:
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> bool:
        pass

    @property
    def settings(self) -> JwtClientSettings:
        pass