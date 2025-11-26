from sqlmodel import Column, Field, SQLModel, UniqueConstraint

from app.models.role import Role
from sqlalchemy import Enum as SAEnum, null

role_enum = SAEnum(
    Role, name="role_enum", values_callable=lambda obj: [e.value for e in obj] 
) 

class User(SQLModel,table=True):
    __table_args__ = (UniqueConstraint("username"),)
    id:Field(default=None,primary_key=True)  
    firstname:str=Field(nullable=False)
    lastname:str=Field(nullable=False)
    username: str = Field(nullable=False, index=True)
    password: str = Field(min_length=8, nullable=False)
    is_active: bool = Field(default=True)
    role: Role = Field(
        sa_column=Column(role_enum, nullable=False),
        default=Role.USER,
    )
    