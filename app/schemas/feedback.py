# app/schemas/feedback.py
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel

from app.schemas.comment import CommentRead


# ---------- Base ----------

class FeedbackBase(SQLModel):
    title: str
    description: Optional[str] = None


# ---------- Create / Update ----------

class FeedbackCreate(FeedbackBase):
    """
    Body for: POST /products/{product_id}/feedback
    org_id + product_id + created_by come from path/auth.
    """
    pass


class FeedbackUpdate(SQLModel):
    """
    Body for: PATCH /feedback/{feedback_id}
    """
    title: Optional[str] = None
    description: Optional[str] = None
    # if later you allow status changes from API, add:
    # status: Optional[str] = None


# ---------- Read ----------

class FeedbackRead(FeedbackBase):
    id: int
    org_id: int
    product_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------- Nested read variants ----------



class FeedbackReadWithComments(FeedbackRead):
    comments: List["CommentRead"] = []

    class Config:
        from_attributes = True
