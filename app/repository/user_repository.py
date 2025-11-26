from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User
class UserRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    # async def createUser(self,user:User)->User:
    #     self.session.add(user)
    #     await self.session.commit()
    #     await self.session.refresh(user)
    #     return user
    
    async def getUserByUserName(self,username:str)->Optional[User]:
        user= await self.session.exec(select(User).where(User.username==username))
        return user.first()
    
    async def getUserById(self,id:int)->Optional[User]:
        user=await self.session.exec(select(User).where(User.id==id))
        return user.first()
    
    async def save(self,user:User)->User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def deleteUser(self,user:User):
        await self.session.delete(user)
        await self.session.commit()