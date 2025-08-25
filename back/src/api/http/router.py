from fastapi import APIRouter
from api.http.dev.object_container_statistics import router as object_container_stats_router
from api.http.dev.main_db_test import router as main_db_test_router
from api.http.dev.user import router as user_router
from api.http.auth.registration_confirm_code import router as registration_confirm_code_router

router = APIRouter()

#auth
router.include_router(registration_confirm_code_router)

#dev
router.include_router(object_container_stats_router)
router.include_router(main_db_test_router)
router.include_router(user_router)