from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.enums import OrganizationStatus, SystemRole
from app.repository.role_repo import RoleRepo

class RoleService:
    def __init__(self,session:AsyncSession):
        self.repo=RoleRepo(session)
    async def getIdFromRoleKey(self,key:SystemRole):
        return await self.repo.getIdFromRoleKey(key)