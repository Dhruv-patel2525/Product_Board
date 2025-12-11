from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import Column, Field, Relationship, SQLModel
from sqlalchemy import DateTime, func

from app.models.products import Product

if TYPE_CHECKING:
    from app.models.invitation import Invitation


class User(SQLModel,table=True):
    __tablename__="users"
    id:int | None=Field(default=None,primary_key=True)  
    name:str=Field(nullable=False)
    username: str = Field(nullable=False, index=True,unique=True)
    password_hash: str = Field( nullable=False)
    is_active: bool = Field(default=True)
    created_at:datetime = Field(
        sa_column=Column(DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
        )
    )
    updated_at:datetime=Field(
        sa_column=Column(DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
        )
    )
    accepted_invitations:list["Invitation"]=Relationship(
        back_populates="accepted_user"
    )
    products:list["Product"]=Relationship(back_populates="created_by_user")
    