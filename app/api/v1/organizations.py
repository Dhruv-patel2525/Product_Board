from importlib.resources import Anchor
from typing import Annotated
from fastapi import APIRouter, Depends
from app.core.db import get_session
from app.core.dep import get_current_user, require_org_permission
from app.models import user
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.organization import OrganizationCreate, OrganizationOut
from sqlmodel.ext.asyncio.session import AsyncSession
from app.service.organization_service import OrganizationService

def get_service(session:AsyncSession=Depends(get_session)):
    return OrganizationService(session)

router=APIRouter(prefix="/org",tags=['Organization'])

@router.get("/",response_model=ApiResponse[list[OrganizationOut]])
async def getMyOrganisation(current_user:Annotated[User,Depends(get_current_user)],service:OrganizationService=Depends(get_service))->ApiResponse[list[OrganizationOut]]:
    organization=await service.getOrganizationsByUserId(user_id=current_user.id)
    return ApiResponse(success=True,data=organization)

@router.post("/",response_model=ApiResponse[OrganizationOut])
async def create_organization(current_user:Annotated[User,Depends(get_current_user)],
                              organization_request:OrganizationCreate,
                              service:OrganizationService=Depends(get_service))->ApiResponse[OrganizationOut]:
    organization=await service.create_organization(organization_request,user_id=current_user.id)
    return ApiResponse(success=True,data=organization)

@router.put("/{id}",
            response_model=ApiResponse[OrganizationOut])
async def updateOrganization(id:int,
                             current_user:Annotated[User,Depends(require_org_permission("org.manage_settings"))],
                             organization_request:OrganizationCreate,
                             service:OrganizationService=Depends(get_service))->ApiResponse[OrganizationOut]:
    organization_response=await service.updateOrganization(organization_request,org_id=id,user_id=current_user.id)
    return ApiResponse(success=True,data=organization_response)

@router.delete("/{id}",
               response_model=ApiResponse[str])
async def delete_organization(id:int,
                              current_user:Annotated[User,Depends(require_org_permission("org.manage_settings"))],
                              service:Annotated[OrganizationService,Depends(get_service)])->ApiResponse[str]:
    await service.delete_organization(org_id=id,user_id=current_user.id)
    return ApiResponse(success=True,data="Deleted successfully")