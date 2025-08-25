from datetime import datetime, UTC

from auth.errors import ValidationError, EmailSendingError
from auth.element.user_auth_confirm_code_settings.user_auth_confirm_code_settings import UserAuthConfirmCodeSettings
from auth.element.user_auth_confirm_code.user_auth_confirm_code import UserAuthConfirmCode
from infra.tool.email_sender.email_sender import EmailSender


async def send(
    instance: UserAuthConfirmCode, 
    settings: UserAuthConfirmCodeSettings,
    email_sender: EmailSender, 
    tx,
    subject: str = None,
    html_template: str = None
):
    now = datetime.now(UTC)
    now_timestamp = now.isoformat()
    action = "send"
    update_data = None
    
    try:
        if now >= instance.expires_at:
            error_message = "Срок действия кода подтверждения истек"
            instance.add_history_entry(action, now_timestamp, False, error_message)
            update_data = {
                "is_sent": False,
                "sending_at": now,
                "sending_error": error_message,
                "history": instance.history,
            }
            raise ValidationError(error_message, error_code="CONFIRM_CODE_EXPIRED")
        
        if instance.sending_attempts_count >= settings.sending_max_attempts_count:
            error_message = f"Превышен лимит попыток отправки ({settings.sending_max_attempts_count})"
            instance.add_history_entry(action, now_timestamp, False, error_message)
            update_data = {
                "is_sent": False,
                "sending_at": now,
                "sending_error": error_message,
                "history": instance.history,
            }
            raise ValidationError(error_message, error_code="SENDING_ATTEMPTS_EXCEEDED")
        
        default_html_template = "<p>Ваш код подтверждения: <strong>{confirm_code}</strong></p>"
        
        email_subject = subject or settings.sending_subject
        html_body = (html_template or default_html_template).format(confirm_code=instance.confirm_code)
        
        await email_sender.send_html_message([instance.auth_email], email_subject, html_body)
        
        instance.add_history_entry(action, now_timestamp, True)
        
        update_data = {
            "is_sent": True,
            "sending_at": now,
            "sending_attempts_count": instance.sending_attempts_count + 1,
            "sending_error": None,
            "history": instance.history,
        }
        
    except Exception as e:
        if update_data is None:
            error_message = str(e)
            instance.add_history_entry(action, now_timestamp, False, error_message)
            update_data = {
                "is_sent": False,
                "sending_at": now,
                "sending_attempts_count": instance.sending_attempts_count + 1,
                "sending_error": error_message,
                "history": instance.history,
            }
            
            if not isinstance(e, (ValidationError, EmailSendingError)):
                raise EmailSendingError(
                    "Временная ошибка отправки email. Код подтверждения сохранен, повторите попытку позже.",
                    "EMAIL_SENDING_FAILED"
                )
        
        raise
    finally:
        if update_data:
            await instance.update(tx=tx, **update_data)
