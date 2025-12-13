from sqlite3 import IntegrityError
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import NotFoundException
from app.models.enums import FeedbackStatus
from app.models.feedback import FeedBack
from app.models.feedback_votes import FeedBackVote
from app.repository.feedback_repository import FeedBackRepository
from app.repository.product_repository import ProductRepository
from app.schemas.feedback import FeedbackCreate, FeedbackRead, FeedbackStatusUpdate, FeedbackUpdate, FeedbackVoteCreate
from app.schemas.users import AuthenticatedUser
class FeedBackService:
    def __init__(self,session:AsyncSession):
        self.repo=FeedBackRepository(session)
        self.product_repo=ProductRepository(session)
    async def get_feedback_by_id(self,org_id:int,product_id:int,feedback_id:int)->FeedbackRead:
        product=await self.product_repo.get_product_by_product_id(org_id=org_id,product_id=product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Product not found for Id")
        feedback=await self.repo.get_feedback_by_id(org_id,product_id,feedback_id)
        if not feedback:
            raise NotFoundException(message="Feedback Not Found", details="Feedback not found by id")

        return FeedbackRead.model_validate(feedback)
    async def get_feedback_list(self,org_id:int,product_id:int)->list[FeedbackRead]:
        product=await self.product_repo.get_product_by_product_id(org_id=org_id,product_id=product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Product not found for Id")
        feedback_list=await self.repo.get_feedback_by_list(org_id,product_id)
        feedback_read_list=list()
        for feedback in feedback_list:
            feedback_read_list.append(FeedbackRead.model_validate(feedback))
        return feedback_read_list
    async def create_feedback(self,org_id:int,product_id:int,feedback_create:FeedbackCreate,current_user:AuthenticatedUser)->FeedbackRead:
        product=await self.product_repo.get_product_by_product_id(org_id=org_id,product_id=product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Product not found for Id")
        feedback=FeedBack(**feedback_create.model_dump(),created_by=current_user.id,org_id=org_id,product_id=product_id,status=FeedbackStatus.NEW)
        feedback_created=await self.repo.save(feedback)
        return FeedbackRead.model_validate(feedback_created)
    async def update_feedback(self,org_id:int,product_id:int,feedback_id:int,feedback_update:FeedbackUpdate,current_user:AuthenticatedUser)->FeedbackRead:
        
        product=await self.product_repo.get_product_by_product_id(org_id=org_id,product_id=product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Product not found for Id")
        feedback=await self.repo.get_feedback_by_id(org_id,product_id,feedback_id)
        if not feedback:
            raise NotFoundException(message="FeedBack Not Found",details="Feedback not found by id")
        user_perms=getattr(current_user,"org_permissions",set())
        if "feedback.edit_all" not in user_perms:
            if "feedback.edit_own" not in user_perms:
                raise HTTPException(status_code=403,detail="Not allowed to edit feedback")
            if feedback.created_by!=current_user.id:
                raise HTTPException(status_code=403,detail="Cannot edit other's feedback")

        for key,value in feedback_update.model_dump(exclude_unset=True).items():
            setattr(feedback,key,value)
        feedback_updated=await self.repo.save(feedback)
        return FeedbackRead.model_validate(feedback_updated)
    async def delete_feedback(self,org_id:int,product_id:int,feedback_id:int,current_user:AuthenticatedUser):

        product=await self.product_repo.get_product_by_product_id(org_id=org_id,product_id=product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Product not found for Id")
        feedback=await self.repo.get_feedback_by_id(org_id,product_id,feedback_id)
        if not feedback:
            raise NotFoundException(message="FeedBack Not Found",details="Feedback not found by id")
        user_perms=getattr(current_user,"org_permissions",set())
        if "feedback.delete_all" not in user_perms:
            if "feedback.delete_own" not in user_perms:
                raise HTTPException(status_code=403,detail="Not allowed to delete feedback")
            if feedback.created_by!=current_user.id:
                raise HTTPException(status_code=403,detail="Cannot delete other's feedback")

        await self.repo.delete(feedback)
    async def update_status(self,org_id:int,product_id:int,feedback_id:int,feedback_status_update:FeedbackStatusUpdate,current_user:AuthenticatedUser)->FeedbackRead:
        product=await self.product_repo.get_product_by_product_id(org_id=org_id,product_id=product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Product not found for Id")
        feedback=await self.repo.get_feedback_by_id(org_id,product_id,feedback_id)
        if not feedback:
            raise NotFoundException(message="FeedBack Not Found",details="Feedback not found by id")
        setattr(feedback,"status",feedback_status_update.status)
        feedback_updated=await self.repo.save(feedback)
        return FeedbackRead.model_validate(feedback_updated)
    async def upvote_feedback(self,org_id:int,product_id:int,feedback_id:int,feedback_vote_create:FeedbackVoteCreate,current_user:AuthenticatedUser)->int:
        feedback=await self.repo.get_feedback_by_id(org_id,product_id,feedback_id)
        if not feedback:
            raise NotFoundException(message="FeedBack Not Found",details="Feedback not found by id")
        feedback_vote=await self.repo.get_feedback_vote_by_id(feedback_id=feedback_id,user_id=current_user.id)
        if feedback_vote:
            if feedback_vote.value==feedback_vote_create.value:
                return await self.get_feedback_votes_counts(org_id=org_id,product_id=product_id,feedback_id=feedback_id)
            setattr(feedback_vote,"value",feedback_vote_create.value)
        else:
            feedback_vote=FeedBackVote(
                feedback_id=feedback.id,
                user_id=current_user.id,
                value=feedback_vote_create.value
            )
        try:
            await self.repo.upvote_feedback(feedback_vote)
        except IntegrityError as e:
            self.session.rollback()
            return await self.get_feedback_votes_counts(org_id=org_id,product_id=product_id,feedback_id=feedback_id)
        
    async def get_feedback_votes_counts(self,org_id:int,product_id:int,feedback_id)->int:
        feedback=await self.repo.get_feedback_by_id(org_id,product_id,feedback_id)
        if not feedback:
            raise NotFoundException(message="FeedBack Not Found",details="Feedback not found by id")
        count=await self.repo.get_feedback_vote_count(feedback_id)
        return count

