from datetime import datetime

from auth.abc.auth_element import AuthElement
from auth.element.user_auth_confirm_code.repository import UserAuthConfirmCodeRepository


class UserAuthConfirmCode(AuthElement):
    _repository_class = UserAuthConfirmCodeRepository

    user_id: int | None = None
    state_id: int
    reason_id: int
    ip_address: str | None = None
    confirm_code: str
    sending_error: str | None = None
    attempts_count: int = 0
    last_attempt_at: datetime | None = None
    expires_at: datetime
