from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text, DateTime, func, ForeignKeyConstraint
if TYPE_CHECKING:
    from app.models.feedback import FeedBack

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    __table_args__ = (
        ForeignKeyConstraint(
            ["feedback_id", "org_id"],
            ["feedback.id", "feedback.org_id"],
            name="fk_comments_feedback_org",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(foreign_key="organization.id", nullable=False)
    feedback_id: int = Field(nullable=False)  
    user_id: int = Field(foreign_key="users.id", nullable=False)

    body: str = Field(sa_column=Column(Text, nullable=False))

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )

    feedback: Optional["FeedBack"] = Relationship(back_populates="comments")