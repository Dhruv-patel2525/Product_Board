from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.feedback import FeedBack
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
        
