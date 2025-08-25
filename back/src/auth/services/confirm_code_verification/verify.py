from datetime import datetime, UTC

from auth.element.user_auth_confirm_code.user_auth_confirm_code import UserAuthConfirmCode
from auth.element.user_auth_confirm_code_settings.user_auth_confirm_code_settings import UserAuthConfirmCodeSettings
from auth.errors import ValidationError


async def verify(
    instance: UserAuthConfirmCode,
    settings: UserAuthConfirmCodeSettings,
    received_confirm_code: str,
    tx,
):
    now = datetime.now(UTC)
    now_timestamp = now.isoformat()
    action = "verify"
    
    if now >= instance.expires_at:
        error_message = "Срок действия кода подтверждения истек"
        
        instance.add_history_entry(action, now_timestamp, False, error_message)
        
        update_data = {
            "is_verified": False,
            "verification_at": now,
            "verification_error": error_message,
            "history": instance.history,
        }
        
        await instance.update(tx=tx, **update_data)
        raise ValidationError(error_message, error_code="CONFIRM_CODE_EXPIRED")
    
    if instance.verification_attempts_count >= settings.verification_max_attempts_count:
        error_message = f"Превышен лимит попыток подтверждения ({settings.verification_max_attempts_count})"
        
        instance.add_history_entry(action, now_timestamp, False, error_message)
        
        update_data = {
            "is_verified": False,
            "verification_at": now,
            "verification_error": error_message,
            "history": instance.history,
        }
        
        await instance.update(tx=tx, **update_data)
        raise ValidationError(error_message, error_code="VERIFICATION_ATTEMPTS_EXCEEDED")
    
    is_code_valid = received_confirm_code.strip() == instance.confirm_code
    
    error_message = "Неверный код подтверждения" if not is_code_valid else None
    instance.add_history_entry(action, now_timestamp, is_code_valid, error_message)
    
    if is_code_valid:
        update_data = {
            "is_verified": True,
            "verification_at": now,
            "verification_attempts_count": instance.verification_attempts_count + 1,
            "verification_error": None,
            "history": instance.history,
        }
    else:
        update_data = {
            "is_verified": False,
            "verification_at": now,
            "verification_attempts_count": instance.verification_attempts_count + 1,
            "verification_error": "Неверный код подтверждения",
            "history": instance.history,
        }
    
    await instance.update(tx=tx, **update_data)
    
    if not is_code_valid:
        raise ValidationError("Неверный код подтверждения", error_code="INVALID_CONFIRM_CODE")
    
    return True
