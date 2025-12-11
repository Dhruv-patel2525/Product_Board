from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.comments import Comment


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, comment: Comment) -> Comment:
        """
        Insert or update a comment.
        Mirrors the pattern you used for FeedBackRepository.save.
        """
        self.session.add(comment)
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def get_comment_by_id(
        self,
        org_id: int,
        feedback_id: int,
        comment_id: int,
    ) -> Optional[Comment]:
        """
        Fetch a single comment by org + feedback + id.
        Ensures we never accidentally cross org/feedback boundaries.
        """
        stmt = (
            select(Comment)
            .where(
                Comment.org_id == org_id,
                Comment.feedback_id == feedback_id,
                Comment.id == comment_id,
            )
        )
        result = await self.session.exec(stmt)
        return result.one_or_none()

    async def get_comment_list(
        self,
        org_id: int,
        feedback_id: int,
    ) -> list[Comment]:
        """
        Fetch all comments for a given feedback in an org.
        You can easily bolt pagination on top of this later.
        """
        stmt = (
            select(Comment)
            .where(
                Comment.org_id == org_id,
                Comment.feedback_id == feedback_id,
            )
            .order_by(Comment.created_at)
        )
        result = await self.session.exec(stmt)
        return result.all()

    async def delete(self, comment: Comment) -> None:
        """
        Hard delete a comment.
        If you ever want soft-delete, this is the place to change behavior.
        """
        await self.session.delete(comment)
        await self.session.flush()
