from auth.element.user_auth_confirm_code.user_auth_confirm_code import UserAuthConfirmCode
from auth.element.user_auth_confirm_code_settings.user_auth_confirm_code_settings import UserAuthConfirmCodeSettings
from infra.tool.email_sender.email_sender import EmailSender
from .create import create as create_func
from .send import send as send_func
from .verify import verify as verify_func


class ConfirmCodeVerification:
    
    @staticmethod
    async def create(
        reason_code: str,
        auth_email: str,
        tx,
        first_name: str = None,
        last_name: str = None,
        middle_name: str = None,
        user_id: int = None,
    ) -> tuple[UserAuthConfirmCode, UserAuthConfirmCodeSettings]:
        return await create_func(
            reason_code=reason_code,
            auth_email=auth_email,
            tx=tx,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            user_id=user_id,
        )
    
    @staticmethod
    async def send(
        instance: UserAuthConfirmCode,
        settings: UserAuthConfirmCodeSettings,
        email_sender: EmailSender, 
        tx,
        subject: str = None,
        html_template: str = None
    ):
        return await send_func(
            instance=instance,
            settings=settings,
            email_sender=email_sender,
            tx=tx,
            subject=subject,
            html_template=html_template,
        )
    
    @staticmethod
    async def verify(
        instance: UserAuthConfirmCode, 
        settings: UserAuthConfirmCodeSettings,
        received_confirm_code: str, 
        tx
    ) -> bool:
        return await verify_func(
            instance=instance,
            settings=settings,
            received_confirm_code=received_confirm_code,
            tx=tx,
        )
