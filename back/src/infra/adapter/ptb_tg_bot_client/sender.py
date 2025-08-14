from adapter.abc.tg_bot_client.sender import Sender as AbstractSender
from adapter.abc.tg_bot_client.application_manager import ApplicationManager


class Sender(AbstractSender):
    def __init__(self, application_manager: ApplicationManager):
        self._application_manager = application_manager
        self._bot = self._application_manager.application.bot
        
    async def send_text(self, chat_id: str | int, text: str) -> None:
        await self._bot.send_message(chat_id=chat_id, text=text)
        
    async def send_photo(self, chat_id: str | int, photo: object, caption: str = None) -> None:
        await self._bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        
    async def send_video(self, chat_id: str | int, video: object, caption: str = None) -> None:
        await self._bot.send_video(chat_id=chat_id, video=video, caption=caption)
        
    async def send_voice(self, chat_id: str | int, voice: object, caption: str = None) -> None:
        await self._bot.send_voice(chat_id=chat_id, voice=voice, caption=caption)
        
    async def send_document(self, chat_id: str | int, document: object, caption: str = None) -> None:
        await self._bot.send_document(chat_id=chat_id, document=document, caption=caption) 