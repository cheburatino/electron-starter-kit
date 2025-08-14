from dataclasses import dataclass


@dataclass
class PostgresConnectionConfig:
    host: str
    port: int
    name: str
    user: str
    password: str
    pool_min_size: int
    pool_max_size: int

    def __post_init__(self):
        if not self.host:
            raise ValueError("host is required")
        if not self.port:
            raise ValueError("port is required")
        if not self.name:
            raise ValueError("name is required")
        if not self.user:
            raise ValueError("user is required")
        if not self.password:
            raise ValueError("password is required")
        if self.pool_min_size < 1:
            raise ValueError("pool_min_size must be greater then 0")
        if self.pool_max_size > 20:
            raise ValueError("pool_max_size must be less then 20")
