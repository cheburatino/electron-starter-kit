from abc import ABC, abstractmethod


class EncryptorAdapter(ABC):
    @abstractmethod
    def generate_encryption_key(self) -> str:
        pass
    
    @abstractmethod
    def encode(self, data: str, encrypt_key_env_var_name: str) -> bytes:
        pass
    
    @abstractmethod
    def decode(self, encrypted_data: bytes, encrypt_key_env_var_name: str) -> str:
        pass
    
    @abstractmethod
    def validate_encryption_key_env_var(self, encrypt_key_env_var_name: str) -> dict:
        pass