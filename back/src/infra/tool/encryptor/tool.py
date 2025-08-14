from functools import lru_cache
from adapter.abc.encryptor.adapter import EncryptorAdapter


class Encryptor:
    def __init__(self, encryptor: EncryptorAdapter):
        self._encryptor = encryptor
    
    def generate_encryption_key(self) -> str:
        return self._encryptor.generate_encryption_key()
    
    def encode(self, data: str, encrypt_key_env_var_name: str) -> bytes:
        return self._encryptor.encode(data, encrypt_key_env_var_name)
    
    def decode(self, encrypted_data: bytes, encrypt_key_env_var_name: str) -> str:
        return self._encryptor.decode(encrypted_data, encrypt_key_env_var_name)
    
    def validate_encryption_key_env_var(self, encrypt_key_env_var_name: str) -> dict:
        return self._encryptor.validate_encryption_key_env_var(encrypt_key_env_var_name)


@lru_cache(maxsize=10)
def get_encryptor(encryptor: EncryptorAdapter) -> Encryptor:
    return Encryptor(encryptor=encryptor) 