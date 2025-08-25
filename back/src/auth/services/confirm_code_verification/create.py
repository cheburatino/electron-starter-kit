import uuid
import secrets
import json
from datetime import datetime, timedelta, UTC

from auth.errors import ValidationError
from auth.element.user_auth_confirm_code.user_auth_confirm_code import UserAuthConfirmCode
from auth.element.user_auth_confirm_code_settings.user_auth_confirm_code_settings import UserAuthConfirmCodeSettings
from auth.catalog.user_auth_confirm_code_reason import UserAuthReason


def _validate_email(email: str) -> None:
    import re
    
    if not email or not email.strip():
        raise ValidationError("Email адрес обязателен", error_code="EMAIL_REQUIRED")
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email.strip()):
        raise ValidationError("Некорректный email адрес", error_code="INVALID_EMAIL")


def _generate_code(alphabet: str, length: int) -> str:
    if not alphabet or length <= 0:
        raise ValueError("Некорректные параметры для генерации кода")
    
    return "".join(secrets.choice(alphabet) for _ in range(length))


async def create(
    reason_code: str,
    auth_email: str,
    tx,
    first_name: str | None = None,
    last_name: str | None = None,
    middle_name: str | None = None,
    user_id: int | None = None,
) -> tuple[UserAuthConfirmCode, UserAuthConfirmCodeSettings]:
    _validate_email(auth_email)
    email = auth_email.strip().lower()
    
    reason_id = await UserAuthReason.get_id_by_code(reason_code, tx=tx)
    if not reason_id:
        raise ValidationError(f"Причина аутентификации с кодом '{reason_code}' не найдена", error_code="REASON_NOT_FOUND")
    
    settings = await UserAuthConfirmCodeSettings.get_by_reason_id(reason_id, tx=tx)
    if not settings:
        raise ValidationError(f"Настройки для reason_id={reason_id} не найдены", error_code="SETTINGS_NOT_FOUND")
    
    token = str(uuid.uuid4())
    code = _generate_code(settings.confirm_code_alphabet, settings.confirm_code_length)
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.confirm_code_ttl_minutes)
    
    history = [{
        "action": "create",
        "timestamp": datetime.now(UTC).isoformat(),
        "ok": True,
        "error_message": None,
    }]
    
    record = await UserAuthConfirmCode.create({
        "user_id": user_id,
        "reason_id": reason_id,
        "auth_email": email,
        "token": token,
        "confirm_code": code,
        "expires_at": expires_at,
        "first_name": first_name,
        "last_name": last_name,
        "middle_name": middle_name,
        "history": json.dumps(history),
    }, tx=tx)
    
    return record, settings
