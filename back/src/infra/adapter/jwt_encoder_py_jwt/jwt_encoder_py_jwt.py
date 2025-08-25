import jwt

from infra.abc.infra_element import InfraElement
from infra.adapter.abc.jwt_encoder.jwt_encoder import JwtEncoder
from .config import JwtEncoderPyJwtConfig


class JwtEncoderPyJwt(InfraElement, JwtEncoder):
    def __init__(self, config: JwtEncoderPyJwtConfig):
        self._config = config

    async def encode_token(self, payload: dict) -> str:
        encoded_jwt = jwt.encode(
            payload,
            self._config.secret_key,
            algorithm=self._config.algorithm_type
        )
        return encoded_jwt

    async def decode_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                self._config.secret_key,
                algorithms=[self._config.algorithm_type]
            )
            return payload
        except jwt.PyJWTError as e:
            print(f"JWT decoding/validation failed: {e}")
            return None



    @property
    def config(self) -> JwtEncoderPyJwtConfig:
        return self._config


def get_user_auth_jwt_encoder() -> JwtEncoderPyJwt:
    return JwtEncoderPyJwt.get_from_container("user_auth_jwt_encoder")
