import asyncio
from core.settings.settings import Settings, get_settings
from tool.tg_bot.tool import get_bot, TgBot
from adapter.abc.tg_bot_client.settings import Settings as TgBotClientSettings


def _get_main_tg_bot() -> TgBot:
    settings: Settings = get_settings()
    main_tg_bot_settings: TgBotClientSettings = settings.get_main_tg_bot_settings()
    
    return get_bot(
        settings=main_tg_bot_settings, 
        title="Electron assistant"
    )


async def start_main_tg_bot():
    print("Инициализация, настройка и запуск Telegram Bot...")
    try:
        bot = _get_main_tg_bot()
        health_status = await bot.health_check()
        if not health_status:
            raise ConnectionError("Telegram Bot health check: FAILED")
        
        bot_task = asyncio.create_task(bot.start())
        print(f"Telegram Bot health check: OK (Bot username: {bot.username})")
        return bot_task
            
    except Exception as e:
        print(f"Критическая ошибка при инициализации или запуске Telegram бота: {e}")
        raise


async def stop_main_tg_bot() -> None:
    try:
        bot = _get_main_tg_bot()
        
        await bot.stop()
        
        await bot.client.application_manager.shutdown()
        
        print(f"Telegram Bot {bot.title} успешно остановлен и ресурсы освобождены.")
    except Exception as e:
        print(f"Ошибка при остановке Telegram бота: {e}") 