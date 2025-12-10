from inspect import _void
from sqlite3 import IntegrityError
from typing import Optional
from app.core.exceptions import ConflictException
from app.models.enums import OrganizationStatus, SystemRole
from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership
from app.repository.organization_membership_repository import OrganizationMembershipRepository
from app.repository.organization_repository import OrganizationRepository
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.organization import OrganizationCreate, OrganizationOut
from app.service.role_service import RoleService

class OrganizationService:
    def __init__(self,session:AsyncSession):
        self.session=session
        self.repo=OrganizationRepository(session)
        self.membership_repo=OrganizationMembershipRepository(session)
        self.role_service=RoleService(session)
    async def getOrganizationsByUserId(self,user_id:int)->Optional[list[OrganizationOut]]:
        organization = await self.repo.getOrganizationsByUserId(user_id)
        if not organization:
            return None
        org_out=list()
        for org in organization:
            org_out.append(OrganizationOut(**org.model_dump()))
        return org_out
    
    async def create_organization(self,organization_request:OrganizationCreate,user_id:int)->OrganizationOut:
        organization=await self.repo.getOrganizationByOrgName(org_name=organization_request.name)
        if organization:
            raise ConflictException(
                message="Organization already exists",
                details="An organization with this name already exists",
            )
        organization=Organization(**organization_request.model_dump(),created_by=user_id)

        try:
            organization_created = await self.repo.save(organization)
        except IntegrityError:
            raise ConflictException(
                message="Organization already exists",
                details="An organization with this name already exists",
            )
        role_id=await self.role_service.getIdFromRoleKey(SystemRole.OWNER)
        org_membership=OrganizationMembership(user_id=user_id,org_id=organization_created.id,role_id=role_id,status=OrganizationStatus.ACTIVE)
        await self.membership_repo.createMembership(org_membership)
        return OrganizationOut(**organization_created.model_dump())

    # need to add role for the one which is not part of my enrolled organization or not an owner of the organization
    async def updateOrganization(self,organization_request:OrganizationCreate,org_id:int,user_id:int)->OrganizationOut:
        organization=await self.repo.getOrganizationByOrgId(org_id)
        if not organization:
            raise ConflictException(message="Organization not Found",details="Organization don't exist for the id")
        for key,value in organization_request.model_dump(exclude_unset=True).items():
            setattr(organization,key,value)
        organization_response=await self.repo.save(organization)
        return OrganizationOut(**organization_response.model_dump())
    
    #Only owner of that organization can delete the organization completely
    async def delete_organization(self,org_id:int,user_id:int)->Optional[any]:
        organization=await self.repo.getOrganizationByOrgId(org_id)
        if not organization:
            raise ConflictException(message="Organization not Found",details="Organization don't exist for the id")
        await self.repo.delete(organization)
        return "Deleted successfully"