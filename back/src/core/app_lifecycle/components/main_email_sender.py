from core.config_manager.config_manager import ConfigManager, Utils as ConfigManagerUtils
from infra.tool.email_sender.tool import EmailSender, Utils as EmailSenderUtils
from infra.system.email.system import SmtpConnectionConfig


def create_main_email_sender() -> EmailSender:
    config_manager: ConfigManager = ConfigManagerUtils.get("config_manager")
    
    connection_config: SmtpConnectionConfig = config_manager.registry.get_config('main_email')
    
    main_email_sender: EmailSender = EmailSenderUtils.factory(
        obj_id="main_email_sender",
        ttl_seconds=-1,
        connection_config=connection_config
    )
    print("Main email sender initialized successfully")
    return main_email_sender
