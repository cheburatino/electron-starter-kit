from auth.abc.auth_element import AuthElement
from auth.element.user.repository import UserRepository
from infra.tool.postgres_client.postgres_client import PostgresClient


class User(AuthElement):
    _repository_class = UserRepository
    
    auth_email: str | None = None
    auth_telegram_id: str | None = None
    person_id: int | None = None
    has_access: bool = False
    
    @classmethod
    async def get_by_email(cls, email: str, db_client: PostgresClient = None, repository: UserRepository = None):
        actual_client = db_client or cls._get_db_client()
        actual_repo = repository or cls._get_repository()
        
        async with actual_client.transaction_manager.transaction():
            data = await actual_repo.get_by_auth_email(email)
            if data:
                instance = cls(str(data['id']), actual_client, actual_repo)
                instance._populate_from_data(data)
                return instance
            return None
    
    @classmethod
    async def get_by_telegram_id(cls, telegram_id: str, db_client: PostgresClient = None, repository: UserRepository = None):
        actual_client = db_client or cls._get_db_client()
        actual_repo = repository or cls._get_repository()
        
        async with actual_client.transaction_manager.transaction():
            data = await actual_repo.get_by_auth_telegram_id(telegram_id)
            if data:
                instance = cls(str(data['id']), actual_client, actual_repo)
                instance._populate_from_data(data)
                return instance
            return None
