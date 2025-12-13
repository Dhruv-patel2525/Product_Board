from typing import Optional
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import user
from app.models.feedback import FeedBack
from app.models.feedback_votes import FeedBackVote
class FeedBackRepository:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def save(self,feedback:FeedBack)->FeedBack:
        self.session.add(feedback)
        await self.session.flush()
        await self.session.refresh(feedback)
        return feedback
    async def get_feedback_by_id(self,org_id:int,product_id:int,feedback_id:int)->Optional[FeedBack]:
        stmt=select(FeedBack).where(FeedBack.org_id==org_id,
                                    FeedBack.product_id==product_id,
                                    FeedBack.id==feedback_id)
        result=await self.session.exec(stmt)
        return result.one_or_none()
    async def get_feedback_by_list(self,org_id:int,product_id:int)->list[FeedBack]:
        stmt=select(FeedBack).where(FeedBack.org_id==org_id,
                                    FeedBack.product_id==product_id)
        result=await self.session.exec(stmt)
        return result.all()
    async def delete(self,feedback:FeedBack)->None:
        await self.session.delete(feedback)
        await self.session.flush()
    async def get_feedback_vote_by_id(self,feedback_id:int,user_id:int)->Optional[FeedBackVote]:
        stmt=select(FeedBackVote).where(FeedBackVote.feedback_id==feedback_id,
                                        FeedBackVote.user_id==user_id)
        result = await self.session.exec(stmt)
        return result.one_or_none()
    async def upvote_feedback(self,feedback_vote:FeedBackVote)->None:
        self.session.add(feedback_vote)
        await self.session.flush()
    
    async def get_feedback_vote_count(self,feedback_id:int)->int:
        stmt=select(func.count()).select_from(FeedBackVote).where(FeedBackVote.feedback_id==feedback_id,
                                        FeedBackVote.value==True)
        result=await self.session.exec(stmt)
        return result.one_or_none()
        