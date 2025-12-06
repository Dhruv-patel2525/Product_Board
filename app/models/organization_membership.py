from datetime import datetime
from sqlalchemy import Column, DateTime, Enum as SAEnum, UniqueConstraint, func
from sqlmodel import Field, SQLModel
from app.models.enums import OrganizationStatus

class OrganizationMembership(SQLModel,table=True):
    __tablename__="oragnizationmembership"
    __table_args__=(UniqueConstraint("user_id","org_id"),) # one user can't have multiple roles in one org 
    id:int|None=Field(default=None,primary_key=True)
    user_id:int= Field(nullable=False,foreign_key="users.id",ondelete="CASCADE")
    org_id:int= Field(nullable=False,foreign_key="organization.id",ondelete="CASCADE")
    role_id:int= Field(nullable=False,foreign_key="role.id")
    status:OrganizationStatus= Field(
        default=OrganizationStatus.ACTIVE,
        sa_column=Column(SAEnum(OrganizationStatus,name='org_membership_status'),nullable=False)
    )
    created_at:datetime= Field(
        sa_column=Column(DateTime(timezone=True),
                         server_default=func.now(),
                         nullable=False)
    )