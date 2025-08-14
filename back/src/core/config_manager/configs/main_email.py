import os
from infra.system.email.system import SmtpConnectionConfig


def _from_env() -> SmtpConnectionConfig:
    username = os.environ.get("MAIN_EMAIL_USERNAME")
    password = os.environ.get("MAIN_EMAIL_PASSWORD")
    from_email = os.environ.get("MAIN_EMAIL_FROM")
    from_name = os.environ.get("MAIN_EMAIL_FROM_NAME")
    server = os.environ.get("MAIN_EMAIL_SERVER")
    port = int(os.environ.get("MAIN_EMAIL_PORT", "587"))
    starttls = os.environ.get("MAIN_EMAIL_STARTTLS", "True").lower() == "true"
    ssl_tls = os.environ.get("MAIN_EMAIL_SSL_TLS", "False").lower() == "true"
    use_credentials = os.environ.get("MAIN_EMAIL_USE_CREDENTIALS", "True").lower() == "true"
    validate_certs = os.environ.get("MAIN_EMAIL_VALIDATE_CERTS", "True").lower() == "true"
    
    if not all([username, password, from_email, server]):
        raise ValueError("Не указаны необходимые параметры для настройки отправки электронной почты")
    
    return SmtpConnectionConfig(
        username=username,
        password=password,
        from_email=from_email,
        from_name=from_name,
        server=server,
        port=port,
        starttls=starttls,
        ssl_tls=ssl_tls,
        use_credentials=use_credentials,
        validate_certs=validate_certs
    )

def get_main_email_config() -> SmtpConnectionConfig:
    return _from_env()