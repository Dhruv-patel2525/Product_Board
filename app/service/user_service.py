from inspect import _void
import logging
from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repository.user_repository import UserRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.common import Token
from app.schemas.users import UserCreate, UserOut, UserUpdate
from app.workers.email_tasks import send_welcome_email
logger=logging.getLogger(__name__)
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
        result = send_welcome_email.delay(email=userOut.username,full_name=userOut.name)
        logger.info("Dispatched welcome email task", extra={"task_id": result.id, "user_id": user.id, "task_name": "email.send_welcome"},)
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
    
    async def updateUser(self,id:int,userUpdate:UserUpdate,current_user:User)->UserOut:
        if current_user.id!=id:
            raise ConflictException(message="Wrong user id for logged in user",details="Invalid user id for logged in user")
        user=await self.repo.getUserById(id)
        if not user:
            raise ConflictException(message="Id not Found",details="User does not exists")
        for key,value in userUpdate.model_dump(exclude_unset=True).items():
            setattr(user,key,value)
        userOut = await self.repo.save(user)
        userOut=UserOut(**userOut.model_dump())
        return userOut
        
    async def deletUser(self,id:int,current_user:User)->_void:
        if(current_user.id!=id):
            raise ConflictException(message="Wrong user id for logged in user",details="Invalid user id for logged in user")
        user=await self.repo.getUserById(id)
        if not user:
            raise ConflictException(message="Id not Found",details="User does not exists")
        await self.repo.deleteUser(user)
        