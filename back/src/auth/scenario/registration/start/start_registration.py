from auth.scenario.registration.start.models import Request
from auth.element.user.user import User
from auth.errors import ResourceConflictError
from auth.services.confirm_code_verification import ConfirmCodeVerification
from auth.element.user_auth_confirm_code.user_auth_confirm_code import UserAuthConfirmCode


class StartRegistration:
    @classmethod
    async def handle(cls, data: Request):
        auth_email = str(data.auth_email).strip().lower()
        first_name = data.first_name.strip()
        last_name = data.last_name.strip() if data.last_name else None

        existing_user = await User.get_by_email(auth_email)
        if existing_user:
            raise ResourceConflictError(
                message="Пользователь с таким email уже существует",
                error_code="USER_ALREADY_EXISTS",
            )

        challenge = ConfirmCodeVerification.start_challenge(
            reason_code="registration",
            channel="email",
            address=auth_email,
            payload={"first_name": first_name, "last_name": last_name},
        )

        user_auth = await UserAuthConfirmCode.create(
            {
                "user_id": None,
                "reason_id": 1,
                "ip_address": None,
                "confirm_code": challenge["code"],
                "sending_error": None,
                "attempts_count": 0,
                "last_attempt_at": None,
                "expires_at": challenge["expires_at"],
            }
        )

        return {
            "session_token": challenge["session_token"],
            "expires_at": challenge["expires_at"],
        }
