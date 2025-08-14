from fastapi import APIRouter, HTTPException

from auth.scenario.registration.start.models import Request as StartRegistrationRequest
from auth.scenario.registration.start.start_registration import StartRegistration
from auth.errors import DomainError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/start-registration")
async def start_registration(data: StartRegistrationRequest):
    try:
        result = await StartRegistration.handle(data)
        return result
    except DomainError as e:
        raise HTTPException(status_code=e.http_status, detail={
            "message": e.message,
            "error_code": e.error_code,
            "meta": e.meta or {},
        })