from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.enums import SystemRole
from app.models.role import Role
class RoleRepo:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def getIdFromRoleKey(self,key:SystemRole):
        stmt=select(Role).where(Role.key==key).limit(1)
        response = await self.session.exec(stmt)
        return response.first().id