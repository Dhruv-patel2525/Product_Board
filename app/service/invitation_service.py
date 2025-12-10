from datetime import datetime, timedelta, timezone, tzinfo
import logging
import secrets
from venv import logger
from app.core.exceptions import ConflictException, NotFoundException
from app.models.enums import InvitationStatus, OrganizationStatus
from app.models.invitation import Invitation
from app.models.organization_membership import OrganizationMembership
from app.models.user import User
from app.repository.invitation_repo import InvitationRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repository.organization_membership_repository import OrganizationMembershipRepository
from app.repository.organization_repository import OrganizationRepository
from app.repository.role_repo import RoleRepo
from app.schemas.invitation import InvitationCreate, InvitationRead
from app.workers.email_tasks import invite_user_to_org
INVITE_EXPIRY_DAYS = 7
logger=logging.getLogger(__name__)
class InvitationService:
    def __init__(self,session:AsyncSession):
        self.repo=InvitationRepository(session)
        self.org_repo=OrganizationRepository(session)
        self.role_repo=RoleRepo(session)
        self.org_membership=OrganizationMembershipRepository(session)
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
        invitation_read=InvitationRead.model_validate(invitation)

        result=invite_user_to_org.delay(invitation_read.model_dump(mode="json"))
        logger.info("Dispatched invite email org", extra={"task_id": result.id, "org_id": org_id, "task_name": "email.invite_user"},)

        return invitation_read
    
    async def get_invitation_by_token(self,token:str)->InvitationRead:
        invitation=await self.repo.get_invitation_by_token(token)
        if not invitation:
            raise NotFoundException(message="Invitation Not Found based on token",details="Token is invalid")
        now=datetime.now(timezone.utc)
        if(now>invitation.expires_at):
            raise ConflictException(message="Token already expired",details="Token expired")
        invitation_read=InvitationRead.model_validate(invitation)
        return invitation_read
    
    async def accept_invitation(self,org_id:int,token:str,current_user:User)->InvitationRead:
        """check status and update it
        match the users if correct user is accepting 
        add an entry to organization membership
        """
        invitation=await self.repo.get_invitation_by_token(token)
        if not invitation:
            raise NotFoundException(message="Invitation Not Found based on token",details="Token is invalid")
        now=datetime.now(timezone.utc)
        if invitation.status!=InvitationStatus.PENDING or invitation.expires_at<now:
            raise ConflictException(message="Invitation is not pending or expired",details="Invitation is expired or not pending")
        if invitation.email!=current_user.username:
            raise ConflictException(message="Email doesn't match with the invitation",details="Trying to accept invitation with wrong email")
        create_membership=OrganizationMembership(
            user_id=current_user.id,
            org_id=org_id,
            role_id=invitation.role_id,
            status=OrganizationStatus.ACTIVE,
        )
        membership_created=await self.org_membership.createMembership(org_membership=create_membership)
        invitation.status=InvitationStatus.ACCEPTED
        invitation_updated = await self.repo.update_status_to_accepted(invitation)
        return InvitationRead.model_validate(invitation_updated)

    
