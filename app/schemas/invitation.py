# app/schemas/invitation.py
from datetime import datetime
from pydantic import BaseModel, EmailStr
from enum import Enum
from app.models.enums import InvitationStatus, SystemRole
from app.schemas.common import ApiResponse

class InvitationCreate(BaseModel):
    email: EmailStr
    role_id: int  
    role_name:SystemRole


class InvitationRead(BaseModel):
    id: int
    org_id: int
    email: EmailStr
    role_id: int
    status: InvitationStatus
    invited_at: datetime
    token:str

    class Config:
        from_attributes = True


class InvitationAccept(BaseModel):
    token: str

class InvitationResponse(ApiResponse[InvitationRead]):
    pass