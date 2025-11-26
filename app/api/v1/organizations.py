from re import L
from typing import Annotated
from fastapi import APIRouter, Depends

from app.core.dep import get_current_user
from app.models.user import User


router=APIRouter(prefix="/org",tags=['Organization'])

@router.get("/")
async def getMyOrganisation(current_user:Annotated[User,Depends(get_current_user)]):
    return "Get My Organisation"