import os
from infra.adapter.abc.tg_bot_client.settings import Settings as TgBotClientSettings


def _from_env() -> TgBotClientSettings:
    token = os.environ.get("MAIN_TG_BOT_TOKEN")
    username = os.environ.get("MAIN_TG_BOT_USERNAME")
    
    if not all([token, username]):
        raise ValueError("Не указаны необходимые параметры для Telegram бота (MAIN_TG_BOT_TOKEN, MAIN_TG_BOT_USERNAME)")
    
    return TgBotClientSettings(
        token=token,
        username=username
    )

def get_main_tg_bot_config() -> TgBotClientSettings:
    return _from_env()