import traceback
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from core.utils.object_utils import ObjectUtils
from infra.adapter.abc.email_sender.adapter import EmailSender
from infra.system.email.system import SmtpConnectionConfig


class EmailSenderFastapiMail(EmailSender):
    def __init__(self, fastapi_mail_connection_config: ConnectionConfig):
        self._fastmail = FastMail(fastapi_mail_connection_config)
        
    async def send_email(self, to: list[str], subject: str, body: str) -> bool:
        try:
            message = MessageSchema(
                subject=subject,
                recipients=to,
                body=body,
                subtype="plain"
            )
            
            await self._fastmail.send_message(message)
            return True
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            print(traceback.format_exc())
            return False
    
    async def send_html_email(self, to: list[str], subject: str, html_body: str) -> bool:
        try:
            message = MessageSchema(
                subject=subject,
                recipients=to,
                body=html_body,
                subtype="html"
            )
            
            await self._fastmail.send_message(message)
            return True
        except Exception as e:
            print(f"Ошибка при отправке HTML-письма: {e}")
            print(traceback.format_exc())
            return False


class Utils(ObjectUtils):
    @classmethod
    def _create(cls, connection_config: SmtpConnectionConfig) -> EmailSenderFastapiMail:
        fastapi_mail_connection_config = ConnectionConfig(
            MAIL_USERNAME=connection_config.username,
            MAIL_PASSWORD=connection_config.password,
            MAIL_FROM=connection_config.from_email,
            MAIL_FROM_NAME=connection_config.from_name,
            MAIL_SERVER=connection_config.server,
            MAIL_PORT=connection_config.port,
            MAIL_STARTTLS=connection_config.starttls,
            MAIL_SSL_TLS=connection_config.ssl_tls,
            USE_CREDENTIALS=connection_config.use_credentials,
            VALIDATE_CERTS=connection_config.validate_certs
        )
        return EmailSenderFastapiMail(fastapi_mail_connection_config=fastapi_mail_connection_config)
