from urllib import response
from httpx import delete
from sqlalchemy import join
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership
class OrganizationRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def getOrganizationsByUserId(self,user_id:int)->list[Organization]:
        stmt=select(Organization).join(OrganizationMembership,OrganizationMembership.org_id==Organization.id).where(OrganizationMembership.user_id==user_id)
        response=await self.session.exec(stmt)
        return list(response.all())
    
    async def getOrganizationByOrgName(self,org_name:str):
        stmt=select(Organization).where(Organization.name==org_name)
        response=await self.session.exec(stmt)
        return response.first()
    
    async def save(self,organization:Organization):
        self.session.add(organization)
        await self.session.flush()
        await self.session.refresh(organization)
        return organization
    
    async def getOrganizationByOrgId(self,org_id:int):
        stmt=select(Organization).where(Organization.id==org_id)
        response = await self.session.exec(stmt)
        return response.first()
    
    async def delete(self,organization:Organization):
        await self.session.delete(organization)
        await self.session.flush()

        
