from functools import lru_cache
from adapter.ptb_tg_bot_client.adapter import get_client
from adapter.abc.tg_bot_client.adapter import TgBotClient
from adapter.abc.tg_bot_client.settings import Settings


class TgBot:
    def __init__(self, client: TgBotClient, title: str):
        self._client = client
        self._title = title
        self._username = client.username
        
        print(f"TgBot инициализирован: title={self._title}, username={self._username}")
        
    async def health_check(self):
        health_check_result = await self._client.application_manager.health_check()
        print(f"Health check для бота {self._title}: {health_check_result}")
        return health_check_result
        
    async def start(self):
        await self._client.start()
        
    async def stop(self):
        await self._client.stop()
        
    @property
    def client(self):
        return self._client
    
    @property
    def title(self):
        return self._title
    
    @property
    def username(self):
        return self._username


@lru_cache(maxsize=10)
def get_bot(settings: Settings, title: str) -> TgBot:
    client = get_client(settings.token, settings.username)
    return TgBot(client=client, title=title)