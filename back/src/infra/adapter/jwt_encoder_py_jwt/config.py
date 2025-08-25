from dataclasses import dataclass
from infra.adapter.abc.jwt_encoder.config import JwtEncoderConfig


@dataclass
class JwtEncoderPyJwtConfig(JwtEncoderConfig):
    secret_key: str
    algorithm_type: str

    def __post_init__(self):
        if not self.secret_key:
            raise ValueError("secret_key is required")
        if not self.algorithm_type:
            raise ValueError("algorithm_type is required")
