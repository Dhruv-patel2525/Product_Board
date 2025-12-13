from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Index, UniqueConstraint, func
from sqlmodel import Field, SQLModel

class FeedBackVote(SQLModel,table=True):
    __tablename__="feedback_vote"
    __table_args__=(
        UniqueConstraint("feedback_id","user_id",name='uq_feedback_id'),#Handling the duplicate votes contraint here at db level 
        Index("ix_feedback_vote_feedback_id","feedback_id")
    )
    id:Optional[int]=Field(default=None,primary_key=True)
    feedback_id:int=Field(foreign_key="feedback.id",nullable=False)
    user_id:int=Field(foreign_key="users.id",nullable=False)
    value:bool=Field(default=True,nullable=False)
    created_at:datetime=Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at:datetime=Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )