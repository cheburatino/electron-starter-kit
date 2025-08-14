from pydantic import BaseModel, EmailStr


class Request(BaseModel):
    auth_email: EmailStr
    first_name: str
    last_name: str | None = None


class Response(BaseModel):
    status: str
    message: str
    data: dict
