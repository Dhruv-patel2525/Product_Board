from typing import Annotated
from fastapi import APIRouter, Depends,status,HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from celery_app import ping
from app.core.db import get_session
from app.core.dep import get_current_user, get_current_user_optional
from app.models.user import User
from app.schemas.common import ApiResponse, Token
from app.schemas.users import AuthenticatedUser, UserCreate, UserOut, UserUpdate
from app.service.user_service import UserService
from celery_app import celery_app
router = APIRouter(prefix="/auth/user", tags=["users"])

def get_service(session:AsyncSession=Depends(get_session)):
    return UserService(session)

@router.get("/")
async def healthCheck(current_user:Annotated[User,Depends(get_current_user)]):
    return {"status": "ok"}

@router.post("/register",response_model=ApiResponse[UserOut])
async def registerUser(userCreate:UserCreate,current_user:Annotated[User|None,Depends(get_current_user_optional)],service:UserService=Depends(get_service))->ApiResponse[UserOut]:
    if current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Logout before creating a new account."
        )

    user=await service.create_user(userCreate)    
    return ApiResponse(success=True,data=user)

@router.post("/login",response_model=ApiResponse[Token])
async def login(formData:Annotated[OAuth2PasswordRequestForm,Depends()],service:UserService=Depends(get_service))->ApiResponse[Token]:
    token=await service.login(username=formData.username,password=formData.password)
    return ApiResponse(success=True,data=token)

@router.post("/token",response_model=Token)
async def token(formData:Annotated[OAuth2PasswordRequestForm,Depends()],service:UserService=Depends(get_service))->Token:
    return await service.login(username=formData.username,password=formData.password)

@router.put("/update-user/{id:int}",response_model=ApiResponse[UserOut])
async def updateUser(id:int,userUpdate:UserUpdate,current_user:Annotated[User,Depends(get_current_user)],service:UserService=Depends(get_service))->ApiResponse[UserOut]:
    userOut=await service.updateUser(id=id,userUpdate=userUpdate,current_user=current_user)
    return ApiResponse(success=True,data=userOut)

@router.delete("/delete-user/{id}",response_model=ApiResponse[str])
async def deletUser(id:int,current_user:Annotated[User,Depends(get_current_user)],service:UserService=Depends(get_service))->ApiResponse[str]:
    await service.deletUser(id=id,current_user=current_user)
    return ApiResponse(success=True,data="Deleted succesfully")

@router.get("/api/v1",response_model=None)
async def call_ping():
    result=ping.delay()
    return {"task_id":result.id}
@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Never block for long here – just report what we know
    return {
        "task_id": task_id,
        "state": result.state,        # PENDING / STARTED / SUCCESS / FAILURE / RETRY
        "result": result.result if result.ready() else None,
    }

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