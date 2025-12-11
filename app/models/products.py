from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, DateTime, func, UniqueConstraint

if TYPE_CHECKING:
    from app.models.product_assignments import ProductAssignment
    from app.models.feedback import FeedBack
    from app.models.organization import Organization
    from app.models.user import User


class Product(SQLModel, table=True):
    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("org_id", "name", name="uq_product_org_name"),
        UniqueConstraint("id", "org_id", name="uq_products_id_org"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(foreign_key="organization.id", nullable=False)
    name: str = Field(
        sa_column=Column(String(255), nullable=False)
    )
    description: Optional[str] = Field(
        sa_column=Column(String(255), nullable=True)
    )
    created_by: int = Field(foreign_key="users.id", nullable=False)
    is_active: bool = Field(default=True, nullable=False)

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

    assignments: List["ProductAssignment"] = Relationship(back_populates="product")
    feedback_items: List["FeedBack"] = Relationship(back_populates="product")
    organization:"Organization"=Relationship(back_populates="products")
    created_by_user:"User"=Relationship(back_populates="products")
