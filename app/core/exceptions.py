from typing import Any, Optional


class AppException(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[Any] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message, details=None):
        super().__init__(
            code="NOT FOUND", message=message, status_code=404, details=details
        )


class ConflictException(AppException):
    def __init__(self, *, message, details=None):
        super().__init__(
            code="CONFLICT", message=message, status_code=409, details=details
        )
