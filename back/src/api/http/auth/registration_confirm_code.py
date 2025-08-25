from fastapi import APIRouter, HTTPException

from auth.scenario.registration.confirm_code.models import Request as SendRequest, VerifyRequest
from auth.scenario.registration.confirm_code.registration_confirm_code import RegistrationConfirmCode
from auth.errors import DomainError
from infra.tool.postgres_client.postgres_client import PostgresClient
from infra.tool.email_sender.email_sender import EmailSender

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registration-confirm-code-start")
async def registration_confirm_code_start(request_data: SendRequest):
    try:
        db_client = PostgresClient.get_from_container("main_db")
        email_sender = EmailSender.get_from_container("main_email_sender")
        
        result = await RegistrationConfirmCode.start(request_data, db_client, email_sender)
        return result
    except DomainError as e:
        raise HTTPException(status_code=e.http_status, detail={
            "error_message": e.message,
            "error_code": e.error_code,
            "meta": e.meta or {},
        })


@router.post("/registration-confirm-code-finish")
async def registration_confirm_code_finish(request_data: VerifyRequest):
    try:
        db_client = PostgresClient.get_from_container("main_db")
        
        result = await RegistrationConfirmCode.finish(request_data, db_client)
        return result
    except DomainError as e:
        raise HTTPException(status_code=e.http_status, detail={
            "error_message": e.message,
            "error_code": e.error_code,
            "meta": e.meta or {},
        })
