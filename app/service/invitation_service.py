from datetime import datetime, timedelta, timezone
import secrets
from time import time_ns
from app.core.config import Settings
from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import create_access_token
from app.models import role
from app.models.enums import InvitationStatus
from app.models.invitation import Invitation
from app.repository.invitation_repo import InvitationRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repository.organization_membership_repository import OrganizationMembershipRepository
from app.repository.organization_repository import OrganizationRepository
from app.repository.role_repo import RoleRepo
from app.schemas.invitation import InvitationCreate, InvitationRead
from app.schemas.users import UserOut
INVITE_EXPIRY_DAYS = 7
class InvitationService:
    def __init__(self,session:AsyncSession):
        self.repo=InvitationRepository(session)
        self.org_repo=OrganizationRepository(session)
        self.role_repo=RoleRepo(session)
    async def create_invitation(self,user_id:int,org_id:int,invited_user:InvitationCreate)->InvitationRead:
        org=await self.org_repo.getOrganizationByOrgId(org_id=org_id)
        if not org:
            raise NotFoundException(message="Organization not found",details="Organization with the id not found")
        #continue with the invitation logic 
        existing=await self.repo.get_pending_by_org_and_email(
            org_id=org_id,
            email=invited_user.email,
        )
        if existing:
            raise ConflictException(message="Pending invitations already exists for this email in this org")
        role_id=await self.role_repo.getIdFromRoleKey(invited_user.role_name)
        if not role_id:
            raise NotFoundException("Role name not found",details="Name not found")
        #Generate token with invite expiry date
        token=secrets.token_urlsafe(32)
        now=datetime.now(timezone.utc)
        expires_at=now+timedelta(days=INVITE_EXPIRY_DAYS)
        # datetime.utcnow()
        invitation=Invitation(
            org_id=org_id,
            email=invited_user.email,
            role_id=role_id,
            token=token,
            status=InvitationStatus.PENDING,
            expires_at=expires_at,
        )
        invitation = await self.repo.add(invitation)
        # accept_url = f"{Settings.FRONTEND_URL}/accept-invite?token={token}"

        return InvitationRead.model_validate(invitation)