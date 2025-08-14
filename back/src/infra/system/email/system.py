from dataclasses import dataclass


@dataclass
class SmtpConnectionConfig:
    username: str
    password: str
    from_email: str
    from_name: str
    server: str
    port: int = 587
    starttls: bool = True
    ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True
    
    def __post_init__(self):
        if not self.username:
            raise ValueError("username is required")
        if not self.password:
            raise ValueError("password is required")
        if not self.from_email:
            raise ValueError("from_email is required")
        if not self.server:
            raise ValueError("server is required")
        if not self.port:
            raise ValueError("port is required")
        if self.port < 1 or self.port > 65535:
            raise ValueError("port must be between 1 and 65535")
