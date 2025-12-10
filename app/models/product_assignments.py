from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
if TYPE_CHECKING:
    from app.models.products import Product

class ProductAssignment(SQLModel, table=True):
    __tablename__ = "product_assignments"
    __table_args__ = (
        # product_id must belong to same org_id
        ForeignKeyConstraint(
            ["product_id", "org_id"],
            ["products.id", "products.org_id"],
            name="fk_product_assignment_product_org",
        ),
        # user_id must be unique per product (a user cannot be assigned twice)
        UniqueConstraint(
            "product_id", "user_id",
            name="uq_product_assignment_product_user",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(foreign_key="organization.id", nullable=False)
    product_id: int = Field(nullable=False)  # FK via table_args (composite)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    role_id: int = Field(foreign_key="role.id", nullable=False)

    product: Optional["Product"] = Relationship(back_populates="assignments")
