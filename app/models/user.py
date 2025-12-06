from datetime import datetime
from sqlmodel import Column, Field, SQLModel
from sqlalchemy import DateTime, func


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
    