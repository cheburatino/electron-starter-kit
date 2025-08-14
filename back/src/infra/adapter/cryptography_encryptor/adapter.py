import os
import base64
from functools import lru_cache
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from adapter.abc.encryptor.adapter import EncryptorAdapter


class CryptographyEncryptor(EncryptorAdapter):
    def __init__(self):
        pass
    
    def generate_encryption_key(self) -> str:
        master_key = os.urandom(32)
        master_key_b64 = base64.b64encode(master_key).decode('utf-8')
        return master_key_b64
    
    def encode(self, data: str, encrypt_key_env_var_name: str) -> bytes:
        key_b64 = os.environ.get(encrypt_key_env_var_name)
        if not key_b64:
            raise ValueError(f"Ключ шифрования с именем {encrypt_key_env_var_name} не найден в переменных окружения")
        
        try:
            key = base64.b64decode(key_b64)
        except Exception:
            raise ValueError(f"Невозможно декодировать ключ шифрования {encrypt_key_env_var_name} из base64")
        
        iv = os.urandom(12)
        cipher = AESGCM(key)
        data_bytes = data.encode('utf-8')
        encrypted_value = cipher.encrypt(iv, data_bytes, None)
        
        encrypted_data = iv + encrypted_value
        return encrypted_data
    
    def decode(self, encrypted_data: bytes, encrypt_key_env_var_name: str) -> str:
        key_b64 = os.environ.get(encrypt_key_env_var_name)
        if not key_b64:
            raise ValueError(f"Ключ шифрования с именем {encrypt_key_env_var_name} не найден в переменных окружения")
        
        try:
            key = base64.b64decode(key_b64)
        except Exception:
            raise ValueError(f"Невозможно декодировать ключ шифрования {encrypt_key_env_var_name} из base64")
        
        iv = encrypted_data[:12]
        value = encrypted_data[12:]
        
        cipher = AESGCM(key)
        decrypted_data = cipher.decrypt(iv, value, None)
        
        return decrypted_data.decode('utf-8')
    
    def validate_encryption_key_env_var(self, encrypt_key_env_var_name: str) -> dict:
        key_b64 = os.environ.get(encrypt_key_env_var_name)
        
        if not key_b64:
            return {
                "ok": False,
                "result": None,
                "err_message": f"Переменная окружения {encrypt_key_env_var_name} не найдена"
            }
        
        if len(key_b64) < 32:
            return {
                "ok": False,
                "result": None,
                "err_message": f"Ключ шифрования в {encrypt_key_env_var_name} слишком короткий: {len(key_b64)} символов (необходимо минимум 32 символа)"
            }
        
        try:
            key = base64.b64decode(key_b64)
            
            if len(key) < 16:
                return {
                    "ok": False,
                    "result": None,
                    "err_message": f"Ключ шифрования в {encrypt_key_env_var_name} недостаточно надежный после декодирования: {len(key)} байт (необходимо минимум 16 байт)"
                }
                
            # Проверка, что ключ может быть использован для AESGCM
            try:
                AESGCM(key)
            except Exception as e:
                return {
                    "ok": False,
                    "result": None,
                    "err_message": f"Ключ шифрования в {encrypt_key_env_var_name} не подходит для алгоритма AESGCM: {str(e)}"
                }
                
        except Exception:
            return {
                "ok": False,
                "result": None,
                "err_message": f"Ключ шифрования в {encrypt_key_env_var_name} не является корректной base64-строкой"
            }
            
        return {
            "ok": True,
            "result": "Ключ шифрования валиден",
            "err_message": None
        }


@lru_cache(maxsize=1)
def get_client() -> CryptographyEncryptor:
    return CryptographyEncryptor() 