from fastapi import APIRouter
from api.http.dev.object_container_statistics import router as object_container_stats_router
from api.http.dev.main_db_test import router as main_db_test_router
# from api.http.dev.email_test import router as email_test_router
from api.http.dev.user import router as user_router
from api.http.dev.catalog_element import router as dev_catalog_router
from api.http.auth.registration import router as auth_registration_router

router = APIRouter()


router.include_router(auth_registration_router)

#dev
router.include_router(object_container_stats_router)
router.include_router(main_db_test_router)
# router.include_router(email_test_router)
router.include_router(user_router)
router.include_router(dev_catalog_router)