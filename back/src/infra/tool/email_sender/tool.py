from core.utils.object_utils import ObjectUtils
from infra.adapter.abc.email_sender.adapter import EmailSender as EmailSenderAdapter
from infra.system.email.system import SmtpConnectionConfig
from infra.adapter.email_sender_fastapi_mail.adapter import EmailSenderFastapiMail, Utils as EmailSenderFastapiMailUtils


class EmailSender:
    def __init__(self, connection_config: SmtpConnectionConfig, sender_adapter: EmailSenderAdapter):
        self._sender_adapter = sender_adapter
        self._connection_config = connection_config
        
    async def send_message(self, to: list[str], subject: str, body: str) -> bool:
        return await self._sender_adapter.send_email(to, subject, body)
        
    async def send_html_message(self, to: list[str], subject: str, html_body: str) -> bool:
        return await self._sender_adapter.send_html_email(to, subject, html_body)
    
    def health_check(self) -> bool:
        try:
            if self._sender_adapter is None:
                return False
                
            return True
        except Exception as e:
            print(f"Ошибка при проверке работоспособности Email-клиента: {e}")
            return False
    
    @property
    def connection_config(self):
        return self._connection_config
    
    @property
    def sender_adapter(self):
        return self._sender_adapter


class Utils(ObjectUtils):
    @classmethod
    def _create(cls, connection_config: SmtpConnectionConfig) -> EmailSender:
        sender_adapter: EmailSenderFastapiMail = EmailSenderFastapiMailUtils.factory(
            obj_id="email_sender_adapter_fastapi_mail", 
            ttl_seconds=3600,
            connection_config=connection_config
        )
        return EmailSender(
            connection_config=connection_config,
            sender_adapter=sender_adapter
        )