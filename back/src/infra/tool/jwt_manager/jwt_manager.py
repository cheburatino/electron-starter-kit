from infra.abc.infra_element import InfraElement
from infra.adapter.abc.jwt_encoder.jwt_encoder import JwtEncoder as JwtEncoderAdapter


class JwtManager(InfraElement):
    def __init__(self, jwt_encoder_adapter: JwtEncoderAdapter):
        if jwt_encoder_adapter is None:
            raise ValueError("jwt_encoder_adapter не может быть None")
            
        self._jwt_encoder_adapter = jwt_encoder_adapter

    @property
    def jwt_encoder_adapter(self) -> JwtEncoderAdapter:
        return self._jwt_encoder_adapter

    async def encode_token(self, payload: dict) -> str:
        return await self._jwt_encoder_adapter.encode_token(payload)

    async def decode_token(self, token: str) -> dict | None:
        return await self._jwt_encoder_adapter.decode_token(token)


def get_user_auth_jwt_manager() -> JwtManager:
    return JwtManager.get_from_container("user_auth_jwt_manager")
