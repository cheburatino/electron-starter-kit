from core.config_manager.config_manager import ConfigManager, Utils as ConfigManagerUtils
from infra.tool.email_sender.email_sender import EmailSender
from infra.adapter.email_sender_fastapi_mail.email_sender_fastapi_mail import EmailSenderFastapiMail
from infra.system.email.system import SmtpConnectionConfig


def create_main_email_sender() -> EmailSender:
    config_manager: ConfigManager = ConfigManagerUtils.get("config_manager")
    
    connection_config: SmtpConnectionConfig = config_manager.registry.get_config('main_email')
    main_email_sender_adapter: EmailSenderFastapiMail = EmailSenderFastapiMail("main_email_sender_adapter", connection_config)
    main_email_sender: EmailSender = EmailSender("main_email_sender", sender_adapter=main_email_sender_adapter)
    print("Main email sender initialized successfully")
    return main_email_sender
