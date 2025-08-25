class DomainError(Exception):
    error_code: str = "DOMAIN_ERROR"
    http_status: int = 500
    message: str | None
    meta: dict | None

    def __init__(self, message: str | None = None, error_code: str | None = None, meta: dict | None = None):
        self.message = message or self.__class__.__name__
        self.error_code = error_code or self.error_code
        self.meta = meta
        super().__init__(self.message)


class ValidationError(DomainError):
    error_code = "VALIDATION_ERROR"
    http_status = 400


class ResourceConflictError(DomainError):
    error_code = "RESOURCE_CONFLICT"
    http_status = 409


class RateLimitError(DomainError):
    error_code = "RATE_LIMIT"
    http_status = 429


class NotFoundError(DomainError):
    error_code = "NOT_FOUND"
    http_status = 404


class ExpiredError(DomainError):
    error_code = "EXPIRED"
    http_status = 410


class AttemptsExceededError(DomainError):
    error_code = "ATTEMPTS_EXCEEDED"
    http_status = 429


class ForbiddenError(DomainError):
    error_code = "FORBIDDEN"
    http_status = 403


class ProviderTemporaryError(DomainError):
    error_code = "PROVIDER_TEMPORARY_ERROR"
    http_status = 503


class ProviderPermanentError(DomainError):
    error_code = "PROVIDER_PERMANENT_ERROR"
    http_status = 400


class InternalError(DomainError):
    error_code = "INTERNAL_ERROR"
    http_status = 500


class EmailSendingError(DomainError):
    error_code = "EMAIL_SENDING_ERROR"
    http_status = 500
