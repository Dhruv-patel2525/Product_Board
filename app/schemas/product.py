# app/schemas/product.py
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel

from app.schemas.feedback import FeedbackRead


# ---------- Base ----------

class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


# ---------- Create / Update ----------

class ProductCreate(ProductBase):
    """
    Body for: POST /orgs/{org_id}/products
    org_id + created_by come from path/auth, not from client.
    """
    pass


class ProductUpdate(SQLModel):
    """
    Body for: PATCH/PUT /products/{product_id}
    All fields optional for partial update.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None



class ProductRead(ProductBase):
    id: int
    org_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # allow reading from ORM objects


# ---------- Nested read variants ----------

# Forward-declare to avoid circular imports
# class FeedbackRead(SQLModel):
#     pass


class ProductReadWithFeedback(ProductRead):
    feedback_items: List["FeedbackRead"] = []

    class Config:
        from_attributes = True
