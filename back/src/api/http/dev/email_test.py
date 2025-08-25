from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from back.src.infra.tool.email_sender.email_sender import EmailSender, Utils as EmailSenderUtils

router = APIRouter(prefix="/dev/email", tags=["dev", "email"])


class SendTestEmailRequest(BaseModel):
    to: list[EmailStr]
    subject: str
    body: str


class SendTestHtmlEmailRequest(BaseModel):
    to: list[EmailStr]
    subject: str
    html_body: str


@router.post("/send-email")
async def send_test_email(request: SendTestEmailRequest):
    """Отправить тестовое текстовое письмо"""
    try:
        email_sender: EmailSender = EmailSenderUtils.get("main_email_sender")
        if not email_sender:
            raise HTTPException(status_code=503, detail="EmailSender не инициализирован")
        
        success = await email_sender.send_message(
            to=request.to,
            subject=request.subject,
            body=request.body
        )
        
        if success:
            return {"status": "success", "message": "Письмо успешно отправлено"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка при отправке письма")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки письма: {str(e)}")


@router.post("/send-html-email")
async def send_test_html_email(request: SendTestHtmlEmailRequest):
    """Отправить тестовое HTML письмо"""
    try:
        email_sender: EmailSender = EmailSenderUtils.get("main_email_sender")
        if not email_sender:
            raise HTTPException(status_code=503, detail="EmailSender не инициализирован")
        
        success = await email_sender.send_html_message(
            to=request.to,
            subject=request.subject,
            html_body=request.html_body
        )
        
        if success:
            return {"status": "success", "message": "HTML письмо успешно отправлено"}
        else:
            raise HTTPException(status_code=500, detail="Ошибка при отправке HTML письма")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки HTML письма: {str(e)}")


@router.get("/health-check")
async def email_health_check():
    """Проверить работоспособность email отправителя"""
    try:
        email_sender: EmailSender = EmailSenderUtils.get("main_email_sender")
        if not email_sender:
            raise HTTPException(status_code=503, detail="EmailSender не инициализирован")
        
        is_healthy = await email_sender.health_check()
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "email_sender_initialized": True,
            "health_check_passed": is_healthy
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "email_sender_initialized": False,
            "health_check_passed": False,
            "error": str(e)
        } 