from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class Role(SQLModel,table=True):
    __tablename__="role"
    id:int|None=Field(default=None,primary_key=True)
    key:str=Field(nullable=False)
    description:str|None=Field(default=None,nullable=True)
    org_id:int|None=Field(default=None,foreign_key="organization.id",nullable=True)
    is_system:bool=Field(default=True,nullable=False)
    created_at:datetime=Field(
        sa_column=Column(DateTime(timezone=True),
                         server_default=func.now(),
                         nullable=False),
        
    )