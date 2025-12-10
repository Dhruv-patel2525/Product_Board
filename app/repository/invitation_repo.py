from typing import Optional
from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.enums import InvitationStatus
from app.models.invitation import Invitation
class InvitationRepository:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def get_pending_by_org_and_email(self,org_id:int,email:EmailStr)->Optional[Invitation]:
        stmt=select(Invitation).where(Invitation.org_id==org_id , Invitation.email==email ,Invitation.email==InvitationStatus.PENDING)
        invitation_response=await self.session.exec(stmt)
        return invitation_response.one_or_none()
    async def add(self,invitation:Invitation)->Invitation:
        self.session.add(invitation)
        await self.session.flush()
        await self.session.refresh(invitation)
        return invitation
    
    async def get_invitation_by_token(self,token:str)->Optional[Invitation]:
        stmt=select(Invitation).where(Invitation.token==token)
        result=await self.session.exec(stmt)
        return result.one_or_none()
    
    async def update_status_to_accepted(self,invitation:Invitation)->Invitation:
        return await self.add(invitation)
    