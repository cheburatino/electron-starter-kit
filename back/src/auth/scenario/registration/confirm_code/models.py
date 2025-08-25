from pydantic import BaseModel, EmailStr


class Request(BaseModel):
    auth_email: EmailStr
    first_name: str
    last_name: str | None = None
    middle_name: str | None = None


class VerifyRequest(BaseModel):
    token: str
    confirm_code: str
