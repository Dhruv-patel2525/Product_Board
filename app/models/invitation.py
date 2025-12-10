import datetime
import secrets
from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlalchemy import Column, DateTime, Enum, Index, String, UniqueConstraint, func
from sqlmodel import Field, Relationship, SQLModel

from app.models import organization
from app.models.enums import InvitationStatus
if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.role import Role
    from app.models.user import User



class Invitation(SQLModel, table=True):
    __tablename__ = "invitation"
    __table_args__=(
        # enforce "one pending per org+email" in service layer.
        UniqueConstraint("org_id","email","status",name="uq_invitation_org_email_status"),
        Index("ix_invitation_org_id_status","org_id","status"),
        Index("ix_invitation_email","email"),
    )

    id: int = Field(default=None, primary_key=True)
    org_id: int = Field(foreign_key="organization.id", ondelete="CASCADE")

    email: EmailStr = Field(default=None, nullable=False)

    role_id: int = Field(foreign_key="role.id", nullable=False)

    token: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False)
    )

    status: InvitationStatus = Field(
        default=InvitationStatus.PENDING,
        sa_column=Column(
            Enum(InvitationStatus, name="invitation_org_status"),
            nullable=False,
        ),
    )

    invited_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    expires_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    accepted_by: Optional[int] = Field(
        default=None,
        foreign_key="users.id",
        nullable=True,
    )

    accepted_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    organization:"Organization"=Relationship(back_populates="invitations")
    role:"Role"=Relationship(back_populates="invitations")
    accepted_user:Optional["User"]=Relationship(back_populates="accepted_invitations")
