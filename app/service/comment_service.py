from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import NotFoundException
from app.models.comments import Comment
from app.repository.comment_repo import CommentRepository
from app.repository.product_repository import ProductRepository
from app.repository.feedback_repository import FeedBackRepository
from app.schemas.comment import CommentRead, CommentCreate, CommentUpdate
from app.schemas.users import AuthenticatedUser

class CommentService:
    def __init__(self, session: AsyncSession):
        self.repo = CommentRepository(session)
        self.product_repo = ProductRepository(session)
        self.feedback_repo = FeedBackRepository(session)

    async def _ensure_product_and_feedback(
        self,
        org_id: int,
        product_id: int,
        feedback_id: int,
    ):
        """
        Shared validation: product must exist in org,
        feedback must exist under that product + org.
        """
        product = await self.product_repo.get_product_by_product_id(
            org_id=org_id,
            product_id=product_id,
        )
        if not product:
            raise NotFoundException(
                message="Product Not Found",
                details="Product not found for Id",
            )

        feedback = await self.feedback_repo.get_feedback_by_id(
            org_id=org_id,
            product_id=product_id,
            feedback_id=feedback_id,
        )
        if not feedback:
            raise NotFoundException(
                message="Feedback Not Found",
                details="Feedback not found by id",
            )

        return feedback

    async def get_comment_by_id(
        self,
        org_id: int,
        product_id: int,
        feedback_id: int,
        comment_id: int,
    ) -> CommentRead:
        await self._ensure_product_and_feedback(org_id, product_id, feedback_id)

        comment = await self.repo.get_comment_by_id(
            org_id=org_id,
            feedback_id=feedback_id,
            comment_id=comment_id,
        )
        if not comment:
            raise NotFoundException(
                message="Comment Not Found",
                details="Comment not found by id",
            )

        return CommentRead.model_validate(comment)

    async def get_comment_list(
        self,
        org_id: int,
        product_id: int,
        feedback_id: int,
    ) -> list[CommentRead]:
        await self._ensure_product_and_feedback(org_id, product_id, feedback_id)

        comment_list = await self.repo.get_comment_list(
            org_id=org_id,
            feedback_id=feedback_id,
        )

        # You could use a list comprehension, but I’ll stay close to your style.
        comment_read_list: list[CommentRead] = []
        for comment in comment_list:
            comment_read_list.append(CommentRead.model_validate(comment))

        return comment_read_list

    async def create_comment(
        self,
        org_id: int,
        product_id: int,
        feedback_id: int,
        comment_create: CommentCreate,
        current_user: AuthenticatedUser,
    ) -> CommentRead:
        await self._ensure_product_and_feedback(org_id, product_id, feedback_id)

        comment = Comment(
            **comment_create.model_dump(),
            org_id=org_id,
            feedback_id=feedback_id,
            user_id=current_user.id,
        )

        comment_created = await self.repo.save(comment)
        return CommentRead.model_validate(comment_created)

    async def update_comment(
        self,
        org_id: int,
        product_id: int,
        feedback_id: int,
        comment_id: int,
        comment_update: CommentUpdate,
        current_user: AuthenticatedUser,
    ) -> CommentRead:
        await self._ensure_product_and_feedback(org_id, product_id, feedback_id)

        comment = await self.repo.get_comment_by_id(
            org_id=org_id,
            feedback_id=feedback_id,
            comment_id=comment_id,
        )
        if not comment:
            raise NotFoundException(
                message="Comment Not Found",
                details="Comment not found by id",
            )

        # Permission logic mirrors your feedback service + your business model.
        user_perms = getattr(current_user, "org_permissions", set())
        if "comment.moderate" not in user_perms:
            if "comment.edit_own" not in user_perms:
                raise HTTPException(
                    status_code=403,
                    detail="Not allowed to edit comments",
                )
            if comment.user_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Cannot edit other users' comments",
                )

        for key, value in comment_update.model_dump(exclude_unset=True).items():
            setattr(comment, key, value)

        comment_updated = await self.repo.save(comment)
        return CommentRead.model_validate(comment_updated)

    async def delete_comment(
        self,
        org_id: int,
        product_id: int,
        feedback_id: int,
        comment_id: int,
        current_user: AuthenticatedUser,
    ):
        await self._ensure_product_and_feedback(org_id, product_id, feedback_id)

        comment = await self.repo.get_comment_by_id(
            org_id=org_id,
            feedback_id=feedback_id,
            comment_id=comment_id,
        )
        if not comment:
            raise NotFoundException(
                message="Comment Not Found",
                details="Comment not found by id",
            )

        user_perms = getattr(current_user, "org_permissions", set())
        if "comment.moderate" not in user_perms:
            if "comment.delete_own" not in user_perms:
                raise HTTPException(
                    status_code=403,
                    detail="Not allowed to delete comments",
                )
            if comment.user_id != current_user.id:
                raise HTTPException(
                    status_code=403,
                    detail="Cannot delete other users' comments",
                )

        await self.repo.delete(comment)
