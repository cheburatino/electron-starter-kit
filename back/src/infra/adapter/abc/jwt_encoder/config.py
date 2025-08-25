from abc import ABC


class JwtEncoderConfig(ABC):
    secret_key: str
    algorithm_type: str

