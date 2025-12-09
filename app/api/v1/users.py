from os import login_tty
from typing import Annotated, Any
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import get_session
from app.core.dep import get_current_user
from app.models.user import User
from app.schemas.common import ApiResponse, Token
from app.schemas.users import UserCreate, UserOut, UserUpdate
from app.service.user_service import UserService

router = APIRouter(prefix="/auth/user", tags=["users"])

def get_service(session:AsyncSession=Depends(get_session)):
    return UserService(session)

@router.get("/")
async def healthCheck(current_user:Annotated[User,Depends(get_current_user)]):
    return {"status": "ok"}

@router.post("/register",response_model=ApiResponse[UserOut])
async def registerUser(userCreate:UserCreate,service:UserService=Depends(get_service))->ApiResponse[UserOut]:
    user=await service.createUser(userCreate)
    return ApiResponse(success=True,data=user)

@router.post("/login",response_model=ApiResponse[Token])
async def login(formData:Annotated[OAuth2PasswordRequestForm,Depends()],service:UserService=Depends(get_service))->ApiResponse[Token]:
    token=await service.login(username=formData.username,password=formData.password)
    return ApiResponse(success=True,data=token)

@router.post("/token",response_model=Token)
async def token(formData:Annotated[OAuth2PasswordRequestForm,Depends()],service:UserService=Depends(get_service))->Token:
    return await service.login(username=formData.username,password=formData.password)

@router.put("/update-user/{id:int}",response_model=ApiResponse[UserOut])
async def updateUser(id:int,userUpdate:UserUpdate,service:UserService=Depends(get_service))->ApiResponse[UserOut]:
    userOut=await service.updateUser(id,userUpdate)
    return ApiResponse(success=True,data=userOut)

@router.delete("/delete-user/{id}",response_model=ApiResponse[str])
async def deletUser(id:int,service:UserService=Depends(get_service))->ApiResponse[str]:
    await service.deletUser(id)
    return ApiResponse(success=True,data="Deleted succesfully")

"""
Login User
Register User
Forgot Password?
Register Organization
View Organizations
Create Products inisde orgs 
Create / view /update feedback for product 
with minimal role check
"""