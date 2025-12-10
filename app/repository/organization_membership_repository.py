from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import organization_membership
from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership
class OrganizationMembershipRepository:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def createMembership(self,org_membership:OrganizationMembership):
        self.session.add(org_membership)
        await self.session.flush()
        await self.session.refresh(org_membership)
        return org_membership
    async def get_organization_membership(self,org_id:int,user_id:int)->Optional[OrganizationMembership]:
        stmt=select(OrganizationMembership).where(OrganizationMembership.org_id==org_id and OrganizationMembership.user_id==user_id)
        response =await self.session.exec(stmt)
        return response.one_or_none()