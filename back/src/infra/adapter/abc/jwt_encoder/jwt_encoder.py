from abc import ABC, abstractmethod
from .config import JwtEncoderConfig


class JwtEncoder(ABC):
    def __init__(self, config: JwtEncoderConfig):
        pass

    @abstractmethod
    async def encode_token(self, payload: dict) -> str:
        pass

    @abstractmethod
    async def decode_token(self, token: str) -> dict | None:
        pass

    @property
    @abstractmethod
    def config(self) -> JwtEncoderConfig:
        pass