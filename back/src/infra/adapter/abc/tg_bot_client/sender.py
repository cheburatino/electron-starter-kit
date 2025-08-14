from abc import ABC, abstractmethod
from .application_manager import ApplicationManager


class Sender(ABC):
    @abstractmethod
    def __init__(self, application_manager: ApplicationManager):
        pass

    @abstractmethod
    async def send_text(self, chat_id: str | int, text: str) -> None:
        pass

    @abstractmethod
    async def send_voice(self, chat_id: str | int, voice: object, caption: str = None) -> None:
        pass

    @abstractmethod
    async def send_photo(self, chat_id: str | int, photo: object, caption: str = None) -> None:
        pass    

    @abstractmethod
    async def send_video(self, chat_id: str | int, video: object, caption: str = None) -> None:
        pass

    @abstractmethod
    async def send_document(self, chat_id: str | int, document: object, caption: str = None) -> None:
        pass