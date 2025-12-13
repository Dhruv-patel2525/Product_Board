# app/schemas/feedback.py
from datetime import datetime
# from typing import Optional, List
from typing import Optional, List
from sqlmodel import SQLModel
from app.models.enums import FeedbackStatus
from app.schemas.comment import CommentRead
from pydantic import ConfigDict


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


# ---------- Read ----------

class FeedbackRead(FeedbackBase):
    id: int
    org_id: int
    product_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    status:FeedbackStatus
    model_config = ConfigDict(from_attributes=True)


# ---------- Nested read variants ----------

class FeedbackStatusUpdate(SQLModel):
    status:FeedbackStatus

class FeedbackReadWithComments(FeedbackRead):
    comments: List["CommentRead"] = []
    model_config = ConfigDict(from_attributes=True)

class FeedbackVoteCreate(SQLModel):
    value:bool=True