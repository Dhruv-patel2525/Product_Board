from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth/user", tags=["users"])


@router.get("/")
async def healthCheck():
    return {"status": "ok"}
