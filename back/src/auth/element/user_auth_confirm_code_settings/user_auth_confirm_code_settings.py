from typing import Optional

from auth.abc.auth_element import AuthElement
from auth.element.user_auth_confirm_code_settings.repository import UserAuthConfirmCodeSettingsRepository
from infra.tool.postgres_client.postgres_client import PostgresClient


class UserAuthConfirmCodeSettings(AuthElement):
    _repository_class = UserAuthConfirmCodeSettingsRepository

    reason_id: int

    confirm_code_length: int
    confirm_code_ttl_minutes: int
    confirm_code_alphabet: str

    sending_max_attempts_count: int
    sending_cooldown_seconds: int
    sending_subject: str
    
    verification_max_attempts_count: int
    
    @classmethod
    async def get_by_reason_id(
        cls,
        reason_id: int,
        tx=None,
        db_client: PostgresClient = None,
        repository: UserAuthConfirmCodeSettingsRepository = None
    ) -> Optional["UserAuthConfirmCodeSettings"]:
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()
        
        async with cls._ensure_transaction(tx, actual_db_client) as transaction:
            data = await actual_repository.get_by_reason_id(reason_id, tx=transaction)
            if data:
                instance = cls._instantiate(str(data["id"]), actual_db_client, actual_repository)
                instance._populate_from_data(data)
                return instance
            return None
