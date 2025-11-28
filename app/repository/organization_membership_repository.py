from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization_membership import OrganizationMembership
class OrganizationMembershipRepository:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def createMembership(self,org_membership:OrganizationMembership):
        self.session.add(org_membership)
        await self.session.flush()
        await self.session.refresh(org_membership)
        return org_membership
