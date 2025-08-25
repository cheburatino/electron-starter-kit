from abc import ABC, abstractmethod

from infra.system.email.system import SmtpConnectionConfig


class EmailSender(ABC):
    @abstractmethod
    async def send_email(self, to: list[str], subject: str, body: str) -> bool:
        pass

    @abstractmethod
    async def send_html_email(self, to: list[str], subject: str, html_body: str) -> bool:
        pass

    @property
    def connection_config(self) -> SmtpConnectionConfig:
        pass