from pydantic import BaseModel, EmailStr
from app.models.user import User
from app.schemas.users import UserOut


class OrganizationCreate(BaseModel):
    name: str
    email: EmailStr

class OrganizationOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes=True
