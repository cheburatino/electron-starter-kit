from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth.element.user.user import User

router = APIRouter(prefix="/dev/user", tags=["dev", "user"])


class CreateUserRequest(BaseModel):
    auth_email: str | None = None
    auth_telegram_id: str | None = None
    has_access: bool = False


class GetByContactRequest(BaseModel):
    contact: str


@router.post("/test-create")
async def test_user_create(data: CreateUserRequest):
    try:
        user_data = {}
        if data.auth_email:
            user_data["auth_email"] = data.auth_email
        if data.auth_telegram_id:
            user_data["auth_telegram_id"] = data.auth_telegram_id
        user_data["has_access"] = data.has_access
        
        user = await User.create(user_data)
        
        return {
            "status": "success",
            "message": "User создан в базе данных",
            "data": {
                "id": user.id,
                "auth_email": user.auth_email,
                "auth_telegram_id": user.auth_telegram_id,
                "has_access": user.has_access,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания пользователя: {str(e)}")


@router.get("/test-get/{user_id}")
async def get_user_by_id(user_id: int):
    try:
        user = await User.get_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User не найден в базе данных")
        
        return {
            "status": "success",
            "message": "User получен из базы данных",
            "data": {
                "id": user.id,
                "auth_email": user.auth_email,
                "auth_telegram_id": user.auth_telegram_id,
                "has_access": user.has_access,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения пользователя: {str(e)}")


@router.post("/test-get-by-email")
async def test_get_by_email(data: GetByContactRequest):
    try:
        user = await User.get_by_email(data.contact)
        
        if not user:
            return {
                "status": "success",
                "message": "User с таким email не найден",
                "data": None
            }
        
        return {
            "status": "success", 
            "message": "User найден по email",
            "data": {
                "id": user.id,
                "auth_email": user.auth_email,
                "auth_telegram_id": user.auth_telegram_id,
                "has_access": user.has_access,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска по email: {str(e)}")


@router.post("/test-get-by-telegram")
async def test_get_by_telegram(data: GetByContactRequest):
    try:
        user = await User.get_by_telegram_id(data.contact)
        
        if not user:
            return {
                "status": "success",
                "message": "User с таким Telegram ID не найден",
                "data": None
            }
        
        return {
            "status": "success",
            "message": "User найден по Telegram ID", 
            "data": {
                "id": user.id,
                "auth_email": user.auth_email,
                "auth_telegram_id": user.auth_telegram_id,
                "has_access": user.has_access,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска по Telegram ID: {str(e)}")


@router.get("/test-list")
async def test_get_users_list():
    try:
        users = await User.get_list()
        
        return {
            "status": "success",
            "message": f"Найдено {len(users)} пользователей",
            "data": [
                {
                    "id": user.id,
                    "auth_email": user.auth_email,
                    "auth_telegram_id": user.auth_telegram_id,
                    "has_access": user.has_access,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "updated_at": user.updated_at.isoformat() if user.updated_at else None
                }
                for user in users
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения списка пользователей: {str(e)}")
