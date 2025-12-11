from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Column, DateTime, func, null
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.invitation import Invitation
    from app.models.products import Product


class Organization(SQLModel,table=True):
    __tablename__="organization"
    id:int|None= Field(default=None,primary_key=True)
    name:str=Field(nullable=False,unique=True)
    email:str|None=Field(default=None,nullable=True)
    created_by:int=Field(foreign_key="users.id",ondelete="SET NULL",nullable=True)
    created_at:datetime=Field(
        sa_column=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    )
    invitations:list["Invitation"]=Relationship(back_populates="organization")
    products:list["Product"]=Relationship(back_populates="organization")