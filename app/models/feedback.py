from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import Column, String, DateTime, func, ForeignKeyConstraint,UniqueConstraint

from app.models.enums import FeedbackStatus

if TYPE_CHECKING:
    from app.models.products import Product
    from app.models.comments import Comment
class FeedBack(SQLModel, table=True):
    __tablename__ = "feedback"
    __table_args__ = (
        ForeignKeyConstraint(
            ["product_id", "org_id"],
            ["products.id", "products.org_id"],
            name="fk_feedback_product_org",
        ),
        UniqueConstraint("id", "org_id", name="uq_feedback_id_org"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(foreign_key="organization.id", nullable=False)
    product_id: int = Field(nullable=False) 
    created_by: int = Field(foreign_key="users.id", nullable=False)
    title: str = Field(sa_column=Column(String(255), nullable=False))
    status: FeedbackStatus = Field(default=FeedbackStatus.NEW)
    description: Optional[str] = Field(
        sa_column=Column(String(255), nullable=True)
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )
    product: Optional["Product"] = Relationship(back_populates="feedback_items")
    comments: List["Comment"] = Relationship(back_populates="feedback")