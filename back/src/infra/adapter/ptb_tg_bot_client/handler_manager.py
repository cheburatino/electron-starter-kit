from adapter.abc.tg_bot_client.handler_manager import HandlerManager as AbstractHandlerManager
from telegram.ext import CommandHandler, MessageHandler, filters


class HandlerManager(AbstractHandlerManager):
    def __init__(self, application: object):
        self._application = application
        
    def add_command_handler(self, command: str, handler: callable):
        command_handler = CommandHandler(command, handler)
        self._application.add_handler(command_handler)
        return command_handler
        
    def add_message_handler(self, handler: callable):
        message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handler)
        self._application.add_handler(message_handler)
        return message_handler
    
    def remove_handler(self, handler: object):
        self._application.remove_handler(handler)
        
    @property
    def application(self) -> object:
        return self._application