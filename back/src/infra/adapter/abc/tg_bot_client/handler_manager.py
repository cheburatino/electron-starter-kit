from abc import ABC, abstractmethod


class HandlerManager(ABC):
    @abstractmethod
    def __init__(self, application: object):
        pass

    @abstractmethod
    def add_command_handler(self, command: str, handler: callable):
        pass

    @abstractmethod
    def add_message_handler(self, handler: callable):
        pass
    
    @abstractmethod
    def remove_handler(self, handler: object):
        pass
    
    @property
    @abstractmethod
    def application(self) -> object:
        pass