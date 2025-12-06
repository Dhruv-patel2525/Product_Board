from inspect import _void
from os import access
from re import U
from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repository.user_repository import UserRepository
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.common import Token
from app.schemas.users import UserCreate, UserOut, UserUpdate

class UserService:
    def __init__(self,session:AsyncSession):
        self.repo=UserRepository(session)
    
    async def createUser(self,userCreate:UserCreate)->UserOut:
        user= await self.repo.getUserByUserName(username=userCreate.username)
        if user:
            raise ConflictException(message="Conflict",details="User Already Exists")
        hash_pass=hash_password(userCreate.password)
        user=User(**userCreate.model_dump(exclude="password"),password_hash=hash_pass)
        userOut=await self.repo.save(user) 
        userOut=UserOut(**userOut.model_dump())
        return userOut
    
    async def login(self,username:str,password:str)->Token:
        user=await self.repo.getUserByUserName(username=username)
        if not user:
            raise NotFoundException(message='NOT_FOUND',details="Username not found")
        elif not user.is_active:
            raise NotFoundException(message="Inactive",details="Inactive user")
        elif not verify_password(password,user.password_hash):
            raise ConflictException(message="Incorrect Password",details="Wrong password")
        userout = UserOut(**user.model_dump())
        token = create_access_token(subject=user.id, user=userout)
        return Token(access_token=token)
    
    async def updateUser(self,id:int,userUpdate:UserUpdate)->UserOut:
        user=await self.repo.getUserById(id)
        if not user:
            raise ConflictException(message="Id not Found",details="User does not exists")
        for key,value in userUpdate.model_dump().items():
            setattr(user,key,value)
        userOut = await self.repo.save(user)
        userOut=UserOut(**userOut.model_dump())
        return userOut
        
    async def deletUser(self,id:int)->_void:
        user=await self.repo.getUserById(id)
        if not user:
            raise ConflictException(message="Id not Found",details="User does not exists")
        await self.repo.deleteUser(user)
        