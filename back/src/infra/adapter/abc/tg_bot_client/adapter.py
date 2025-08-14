from abc import ABC, abstractmethod
from .sender import Sender
from .application_manager import ApplicationManager
from .handler_manager import HandlerManager
from .settings import Settings


class TgBotClient(ABC):
    Sender = Sender
    HandlerManager = HandlerManager
    ApplicationManager = ApplicationManager
    
    @abstractmethod
    def __init__(self, settings: Settings):
        pass
    
    @property
    @abstractmethod
    def username(self) -> str | None:
        pass

    @property
    @abstractmethod
    def token(self) -> str:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
    
    @property
    @abstractmethod
    def sender(self) -> Sender:
        pass
    
    @property
    @abstractmethod
    def handler_manager(self) -> HandlerManager:
        pass
    
    @property
    @abstractmethod
    def application_manager(self) -> ApplicationManager:
        pass
