import re
import uuid
import secrets
from datetime import datetime, timedelta, UTC

from auth.errors import ValidationError


class ConfirmCodeVerification:
    code_length: int = 6
    ttl_minutes: int = 15
    max_attempts: int = 3
    resend_cooldown_seconds: int = 60
    alphabet: str = "0123456789"

    @classmethod
    def _generate_code(cls) -> str:
        return "".join(secrets.choice(cls.alphabet) for _ in range(cls.code_length))

    @classmethod
    def _normalize_address(cls, channel: str, address: str) -> str:
        value = address.strip()
        if channel == "email":
            value = value.lower()
        return value

    @classmethod
    def _validate_address(cls, channel: str, address: str) -> None:
        if channel == "email":
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, address):
                raise ValidationError("Некорректный email адрес", error_code="INVALID_EMAIL")

    @classmethod
    def start_challenge(
        cls,
        reason_code: str,
        channel: str,
        address: str,
        payload: dict | None = None,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> dict:
        normalized_address = cls._normalize_address(channel, address)
        cls._validate_address(channel, normalized_address)

        session_token = str(uuid.uuid4())
        code = cls._generate_code()
        expires_at = datetime.now(UTC) + timedelta(minutes=cls.ttl_minutes)

        return {
            "session_token": session_token,
            "code": code,
            "expires_at": expires_at,
            "reason_code": reason_code,
            "channel": channel,
            "address": normalized_address,
            "payload": payload or {},
            "ip": ip,
            "user_agent": user_agent,
        }

    @classmethod
    def verify_challenge(cls, session_token: str, code: str) -> dict:
        if not code or len(code.strip()) != cls.code_length or any(c not in cls.alphabet for c in code.strip()):
            raise ValidationError("Некорректный код подтверждения", error_code="INVALID_CONFIRM_CODE")

        confirmed_at = datetime.now(UTC)
        return {"confirmed_at": confirmed_at}
