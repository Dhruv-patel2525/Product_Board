from fastapi.exceptions import RequestValidationError
from app.api.v1.users import router as user_router
from app.api.v1.organizations import router as org_router
from app.api.v1.invitation import router as inv_router
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from app.core import error_handlers
from app.core.config import get_settings
from app.core.exceptions import AppException


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.PROJECT_NAME, version="0.1.1")
    app.include_router(user_router, prefix="/api/v1")
    app.include_router(org_router,prefix="/api/v1")
    app.include_router(inv_router,prefix="/api/v1")
    return app


app = create_app()
app.add_exception_handler(AppException, error_handlers.app_exception_handler)
app.add_exception_handler(StarletteHTTPException, error_handlers.http_exception_handler)
app.add_exception_handler(
    RequestValidationError, error_handlers.validation_exception_handler
)
app.add_exception_handler(
    IntegrityError, error_handlers.sqlalchemy_integrity_error_handler
)
app.add_exception_handler(Exception, error_handlers.generic_exception_handler)
