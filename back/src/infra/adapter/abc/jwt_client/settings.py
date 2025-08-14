from dataclasses import dataclass


@dataclass
class Settings:
    secret_key: str
    algorithm_type: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    def __hash__(self):
        return hash((
            self.secret_key,
            self.algorithm_type,
            self.access_token_expire_minutes,
            self.refresh_token_expire_days
        ))

    def __eq__(self, other):
        if not isinstance(other, Settings):
            return False
        return (
            self.secret_key == other.secret_key and
            self.algorithm_type == other.algorithm_type and
            self.access_token_expire_minutes == other.access_token_expire_minutes and
            self.refresh_token_expire_days == other.refresh_token_expire_days
        ) 