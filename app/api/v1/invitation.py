from typing import Annotated
from fastapi import APIRouter, Depends
from app.core.db import get_session
from app.core.dep import require_org_permission
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.invitation import InvitationCreate, InvitationRead, InvitationResponse
from app.service.invitation_service import InvitationService
from sqlmodel.ext.asyncio.session import AsyncSession
def get_service(session:AsyncSession=Depends(get_session)):
    return InvitationService(session)
router=APIRouter(prefix="/orgs",tags=['organizations'])
@router.post("/{org_id}/invites",response_model=ApiResponse[InvitationRead])
async def create_invitation(
    org_id:int,
    payload:InvitationCreate,
    current_user:Annotated[User,Depends(require_org_permission("org.manage_members"))],
    invitation_service:Annotated[InvitationService,Depends(get_service)]
)->ApiResponse[InvitationRead]:
    response=await invitation_service.create_invitation(user_id=current_user.id,org_id=org_id,invited_user=payload)
    return ApiResponse(success=True,data=response)
