from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth.catalog.user_auth_confirm_code_reason import (
    UserAuthConfirmCodeReason as Catalog,
)


router = APIRouter(prefix="/dev/catalog/reason", tags=["dev", "catalog", "reason"])


class CreateCatalogItemRequest(BaseModel):
    title: str
    code: str | None = None


class UpdateCatalogItemRequest(BaseModel):
    title: str | None = None
    code: str | None = None


class GetIdByCodeRequest(BaseModel):
    code: str


@router.post("/create")
async def create_catalog_item(data: CreateCatalogItemRequest):
    try:
        item: Catalog = await Catalog.create({"title": data.title, "code": data.code})
        return {
            "message": "Элемент каталога создан",
            "data": {"id": item.id, "title": item.title, "code": item.code},
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/{item_id}")
async def update_catalog_item(item_id: int, data: UpdateCatalogItemRequest):
    try:
        updated = await Catalog.update_by_id(item_id, {"title": data.title, "code": data.code})
        return {
            "message": "Элемент каталога обновлён",
            "data": {"id": updated.id, "title": updated.title, "code": updated.code},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get-id-by-code")
async def get_id_by_code(data: GetIdByCodeRequest):
    try:
        catalog_id = await Catalog.get_id_by_code(data.code)
        return {"code": data.code, "id": catalog_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


