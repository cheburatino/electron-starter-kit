from dataclasses import dataclass


@dataclass
class UserTokenManagerConfig:
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    def __post_init__(self):
        if self.access_token_expire_minutes < 1:
            raise ValueError("access_token_expire_minutes must be greater than 0")
        if self.refresh_token_expire_days < 1:
            raise ValueError("refresh_token_expire_days must be greater than 0")
