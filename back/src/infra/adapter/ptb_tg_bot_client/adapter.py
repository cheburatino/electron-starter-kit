from adapter.abc.tg_bot_client.adapter import TgBotClient
from adapter.abc.tg_bot_client.settings import Settings
from .application_manager import ApplicationManager
from .sender import Sender
from .handler_manager import HandlerManager
from functools import lru_cache


class PtbTgBotClient(TgBotClient):
    Sender = Sender
    HandlerManager = HandlerManager
    ApplicationManager = ApplicationManager
    
    def __init__(self, settings: Settings):
        self._settings = settings
        
        self._application_manager = self.ApplicationManager(token=settings.token)
        self._application_manager.build_application()
        
        self._handler_manager = self.HandlerManager(
            application=self._application_manager.application
        )
        
        self._sender = self.Sender(
            application_manager=self._application_manager
        )
    
    @property
    def username(self) -> str | None:
        return self._settings.username

    @property
    def token(self) -> str:
        return self._settings.token
    
    async def start(self) -> None:
        await self._application_manager.start()

    async def stop(self) -> None:
        await self._application_manager.stop()
    
    @property
    def sender(self) -> Sender:
        return self._sender
    
    @property
    def handler_manager(self) -> HandlerManager:
        return self._handler_manager
    
    @property
    def application_manager(self) -> ApplicationManager:
        return self._application_manager


@lru_cache(maxsize=10)
def get_client(token: str, username: str = None) -> PtbTgBotClient:
    settings = Settings(token=token, username=username)
    return PtbTgBotClient(settings=settings) 