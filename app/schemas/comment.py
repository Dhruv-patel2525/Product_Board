# app/schemas/comment.py
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel
from pydantic import ConfigDict


# ---------- Base ----------

class CommentBase(SQLModel):
    body: str


# ---------- Create ----------

class CommentCreate(CommentBase):
    """
    Body for: POST /feedback/{feedback_id}/comments
    org_id + feedback_id + user_id come from path/auth.
    """
    pass


class CommentUpdate(SQLModel):
    body: Optional[str] = None


# ---------- Read ----------

class CommentRead(CommentBase):
    id: int
    org_id: int
    feedback_id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
