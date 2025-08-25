from contextlib import asynccontextmanager
from core.utils.object_utils import ObjectUtils
from .components.object_container_cleanup import start_object_container_cleanup, stop_object_container_cleanup
from .components.env_manager import create_env_manager
from .components.load_env import load_env
from .components.config_manager import create_config_manager
from .components.main_db import connect_main_db, disconnect_main_db
from .components.main_email_sender import create_main_email_sender
from .components.user_token_manager import start_user_token_manager
# from .components.main_tg_bot import start_main_tg_bot, stop_main_tg_bot

class AppLifecycle:
    def get_lifespan(self):
        @asynccontextmanager
        async def lifespan(app):
            await self.startup()
            yield
            await self.shutdown()
        return lifespan

    async def startup(self):
        await start_object_container_cleanup()
        create_env_manager()
        load_env()
        create_config_manager()
        await connect_main_db()
        create_main_email_sender()
        start_user_token_manager()
        # await start_main_tg_bot()
        # await initialize_electronik()

    async def shutdown(self):
        # await stop_main_tg_bot()
        await disconnect_main_db()
        await stop_object_container_cleanup()

class Utils(ObjectUtils):
    @classmethod
    def _create(cls, **kwargs) -> AppLifecycle:
        return AppLifecycle()
