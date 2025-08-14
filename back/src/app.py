from fastapi import FastAPI
from state.live.object_container.object_container import ObjectContainer

# Инициализируем ObjectContainer в самом начале
ObjectContainer.initialize()

from core.app_lifecycle.app_lifecycle import AppLifecycle, Utils as AppLifecycleUtils
from api.http.router import router
from api.http.server import setup_server

app_lifecycle: AppLifecycle = AppLifecycleUtils.factory(obj_id="app_lifecycle", ttl_seconds=-1)
lifespan = app_lifecycle.get_lifespan()
app = FastAPI(lifespan=lifespan)

setup_server(app)
app.include_router(router)
