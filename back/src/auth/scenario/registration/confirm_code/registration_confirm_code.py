from .models import Request, VerifyRequest
from auth.element.user.user import User
from auth.element.user_auth_confirm_code.user_auth_confirm_code import UserAuthConfirmCode
from auth.element.user_auth_confirm_code_settings.user_auth_confirm_code_settings import UserAuthConfirmCodeSettings
from logic.element.person.person import Person
from auth.errors import ResourceConflictError, ValidationError, EmailSendingError, NotFoundError
from infra.tool.postgres_client.postgres_client import PostgresClient
from infra.tool.email_sender.email_sender import EmailSender
from auth.services.confirm_code_verification.confirm_code_verification import ConfirmCodeVerification
from infra.tool.user_token_manager.user_token_manager import UserTokenManager

class RegistrationConfirmCode:
    @classmethod
    async def start(cls, data: Request, db_client: PostgresClient, email_sender: EmailSender):
        auth_email = str(data.auth_email).strip().lower()
        first_name = data.first_name.strip()
        last_name = data.last_name.strip() if data.last_name else None
        middle_name = data.middle_name.strip() if data.middle_name else None

        tx = await db_client.transaction_manager.begin()
        tx_completed = False
        try:
            existing_user = await User.get_by_auth_email(auth_email, tx=tx)
            if existing_user:
                raise ResourceConflictError(
                    message="Пользователь с таким email уже существует",
                    error_code="USER_ALREADY_EXISTS",
                )

            auth_record, settings = await ConfirmCodeVerification.create(
                reason_code="REGISTRATION",
                auth_email=auth_email,
                tx=tx,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
            )
            
            try:
                await ConfirmCodeVerification.send(auth_record, settings, email_sender, tx)
            except (ValidationError, EmailSendingError) as e:
                await tx.commit()
                tx_completed = True
                raise
            
            await tx.commit()
            tx_completed = True

            return {
                "session_token": auth_record.token,
                "expires_at": auth_record.expires_at,
            }
            
        except Exception:
            if not tx_completed:
                await tx.rollback()
            raise

    @classmethod
    async def finish(cls, data: VerifyRequest, db_client: PostgresClient):
        tx = await db_client.transaction_manager.begin()
        tx_completed = False
        try:
            auth_record = await UserAuthConfirmCode.get_by_token(data.token, tx=tx)
            if not auth_record:
                raise NotFoundError(
                    message="Запись подтверждения не найдена",
                    error_code="CONFIRM_CODE_NOT_FOUND",
                )

            settings = await UserAuthConfirmCodeSettings.get_by_reason_id(auth_record.reason_id, tx=tx)
            if not settings:
                raise NotFoundError(
                    message="Настройки подтверждения не найдены",
                    error_code="SETTINGS_NOT_FOUND",
                )
            
            try:
                result = await ConfirmCodeVerification.verify(
                    instance=auth_record,
                    settings=settings,
                    received_confirm_code=data.confirm_code,
                    tx=tx
                )
                
                person_data = {
                    "first_name": auth_record.first_name,
                    "last_name": auth_record.last_name,
                    "middle_name": auth_record.middle_name,
                }
                person = await Person.create(data=person_data, tx=tx)
                
                user_data = {
                    "person_id": person.id,
                    "auth_email": auth_record.auth_email,
                    "has_access": True,
                }
                user = await User.create(data=user_data, tx=tx)
                
                user_token_manager: UserTokenManager = UserTokenManager.get_from_container("user_token_manager")
                access_token = await user_token_manager.create_access_token(user.id)
                refresh_token, refresh_token_expires_at = user_token_manager.create_refresh_token()
                await user.update(tx=tx, refresh_token=refresh_token, refresh_token_expires_at=refresh_token_expires_at)
                
                await auth_record.update(tx=tx, user_id=user.id)
                
                await tx.commit()
                tx_completed = True
                
                return {
                    "verified": True,
                    "message": "Код подтверждения успешно проверен",
                    "user_id": user.id,
                    "person_id": person.id,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
                
            except ValidationError as e:
                await tx.commit()
                tx_completed = True
                raise
            
        except Exception:
            if not tx_completed:
                await tx.rollback()
            raise
