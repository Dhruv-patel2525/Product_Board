#invitation table
import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, DateTime, Enum, func
from sqlmodel import Field
from app.models.enums import InvitationStatus

class Invitation(BaseModel,table=True):
    __tablename__="invitation"
    id:int=Field(default=None,primary_key=True)
    org_id:int=Field(foreign_key="organization.id",ondelete="CASCADE")
    email:EmailStr=Field(default=None,nullable=True)
    role_id:int=Field(foreign_key="role.id")
    status:InvitationStatus=Field(default=InvitationStatus.PENDING,
                                  sa_column=Column(Enum(InvitationStatus,name="invitation_org_status"),
                                  nullable=False))
    invited_at:datetime=Field(
        sa_column=Column(DateTime(timezone=True),
                         server_default=func.now(),
                         nullable=False
        )
    )
    accepted_by:int=Field(foreign_key="user.id",nullable=True)
    accepted_at:datetime=Field(
        sa_column=Column(DateTime(timezone=True),
                         nullable=True)
    )