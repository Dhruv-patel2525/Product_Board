from typing import Annotated
from fastapi import APIRouter, Depends
from app.core.db import get_session
from app.core.dep import get_current_user, require_org_permission
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.invitation import InvitationCreate, InvitationRead, InvitationResponse
from app.schemas.users import AuthenticatedUser
from app.service.invitation_service import InvitationService
from sqlmodel.ext.asyncio.session import AsyncSession
def get_service(session:AsyncSession=Depends(get_session)):
    return InvitationService(session)
router=APIRouter(prefix="/orgs",tags=['organizations_invitation'])
@router.post("/{org_id}/invites",response_model=ApiResponse[InvitationRead])
async def create_invitation(
    org_id:int,
    payload:InvitationCreate,
    current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("org.manage_members"))],
    invitation_service:Annotated[InvitationService,Depends(get_service)]
)->ApiResponse[InvitationRead]:
    response=await invitation_service.create_invitation(user_id=current_user.id,org_id=org_id,invited_user=payload)
    return ApiResponse(success=True,data=response)

"""this route is unprotected to fetch the organization and invitation detail when hitted
   logged_in_user can get the invitation yes by token 
"""
@router.get("/invites/{token}",response_model=ApiResponse[InvitationRead])
async def get_invitation_by_token(token:str,invitation_service:Annotated[InvitationService,Depends(get_service)])->ApiResponse[InvitationRead]:
    result=await invitation_service.get_invitation_by_token(token)
    return ApiResponse(success=True,data=result)

@router.post("/{org_id}/invites/{token}/accept",response_model=ApiResponse[InvitationRead])
async def accept_invitation(
    org_id:int,
    token:str,
    current_user:Annotated[User,Depends(get_current_user)],
    invitation_service:Annotated[InvitationService,Depends(get_service)]
)->ApiResponse[InvitationRead]:
    result=await invitation_service.accept_invitation(org_id,token,current_user)
    return ApiResponse(success=True,data=result)