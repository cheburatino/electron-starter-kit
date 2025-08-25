from datetime import datetime
from dataclasses import dataclass
import json

from auth.abc.auth_element import AuthElement
from auth.element.user_auth_confirm_code.repository import UserAuthConfirmCodeRepository
from infra.tool.postgres_client.postgres_client import PostgresClient


@dataclass
class History:
    action: str
    timestamp: str
    ok: bool
    error_message: str | None = None


class UserAuthConfirmCode(AuthElement):
    _repository_class = UserAuthConfirmCodeRepository

    reason_id: int

    user_id: int | None = None

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    auth_email: str | None = None
    
    confirm_code: str
    expires_at: datetime
    token: str

    sending_at: datetime | None = None
    is_sent: bool = False
    sending_error: str | None = None
    sending_attempts_count: int = 0

    verification_at: datetime | None = None
    is_verified: bool = False
    verification_error: str | None = None
    verification_attempts_count: int = 0

    history: str | None = None
    
    @property
    def history_entries(self) -> list[History]:
        if not self.history:
            return []
        
        try:
            data = json.loads(self.history)
            return [History(**entry) for entry in data]
        except (json.JSONDecodeError, TypeError):
            return []
    
    def add_history_entry(self, action: str, timestamp: str, ok: bool, error_message: str | None = None):
        
        new_entry = History(action=action, timestamp=timestamp, ok=ok, error_message=error_message)
        entries = self.history_entries
        entries.append(new_entry)
        
        self.history = json.dumps([entry.__dict__ for entry in entries])
    
    
    @classmethod
    async def get_by_token(cls, token: str, tx=None, db_client: PostgresClient = None, repository: UserAuthConfirmCodeRepository = None):
        actual_db_client = db_client or cls._get_db_client()
        actual_repository = repository or cls._get_repository()
        
        async with cls._ensure_transaction(tx, actual_db_client) as transaction:
            data = await actual_repository.get_by_token(token, tx=transaction)
            if data:
                instance = cls._instantiate(str(data["id"]), actual_db_client, actual_repository)
                instance._populate_from_data(data)
                return instance
            return None
