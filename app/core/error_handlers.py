from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError

from app.schemas.common import ApiResponse, ErrorInfo
from app.core.exceptions import AppException


def app_exception_handler(request: Request, exc: AppException):
    error = ErrorInfo(
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(success=False, error=error, data=None).model_dump(),
    )


def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # For plain HTTPException, map status_code to a generic code
    code = "HTTP_ERROR"
    if exc.status_code == 404:
        code = "NOT_FOUND"
    elif exc.status_code == 401:
        code = "UNAUTHORIZED"

    error = ErrorInfo(code=code, message=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(success=False, error=error, data=None).model_dump(),
    )


def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = ErrorInfo(
        code="VALIDATION_ERROR",
        message="Request validation failed",
        details=exc.errors(),  # pydantic error structure
    )
    return JSONResponse(
        status_code=422,
        content=ApiResponse(success=False, error=error, data=None).model_dump(),
    )


def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
    # Don’t leak raw DB error message in prod; log it instead.
    error = ErrorInfo(
        code="DB_INTEGRITY_ERROR",
        message="Database integrity error",
        details=exc.args,
    )
    return JSONResponse(
        status_code=400,
        content=ApiResponse(success=False, error=error, data=None).model_dump(),
    )


def generic_exception_handler(request: Request, exc: Exception):
    # Last-resort catch-all. Log full traceback, return generic message.
    error = ErrorInfo(
        code="INTERNAL_SERVER_ERROR",
        message="Internal server error",
        details=None,
    )
    return JSONResponse(
        status_code=500,
        content=ApiResponse(success=False, error=error, data=None).model_dump(),
    )
