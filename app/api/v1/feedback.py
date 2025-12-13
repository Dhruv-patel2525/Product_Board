from typing import Annotated
from unittest import removeResult
from fastapi import APIRouter,Depends
from app.core.db import get_session
from app.core.dep import require_org_permission
from app.schemas.common import ApiResponse
from app.schemas.feedback import FeedbackCreate, FeedbackRead, FeedbackStatusUpdate, FeedbackUpdate, FeedbackVoteCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.users import AuthenticatedUser
from app.service.feedback_service import FeedBackService
# {"code": "feedback.view", "description": "View feedback items"},
# {"code": "feedback.create", "description": "Create new feedback items"},
# {"code": "feedback.edit_own", "description": "Edit own feedback"},
# {"code": "feedback.edit_all", "description": "Edit all feedback"},
# {"code": "feedback.delete_own", "description": "Delete own feedback"},
# {"code": "feedback.delete_all", "description": "Delete any feedback"},
# {"code": "feedback.change_status", "description": "Change feedback status"},

# {"code": "vote.create", "description": "Add votes to feedback"},
# {"code": "vote.revoke", "description": "Remove own votes"},
# {"code": "vote.view_counts", "description": "View vote counts and analytics"},
def get_service(session:AsyncSession=Depends(get_session)):
    return FeedBackService(session)

router=APIRouter(prefix="/orgs/{org_id}/products/{product_id}/feedback",tags=["Feedback"])

@router.get("/{feedback_id}",response_model=ApiResponse[FeedbackRead])
async def get_feedback_by_product_id(org_id:int,
                                     product_id:int,
                                     feedback_id:int,
                                     current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("feedback.view"))],
                                     feedback_service:Annotated[FeedBackService,Depends(get_service)])->ApiResponse[FeedbackRead]:
    result=await feedback_service.get_feedback_by_id(org_id,product_id,feedback_id)
    return ApiResponse(success=True,data=result)

@router.get("/",response_model=ApiResponse[list[FeedbackRead]])
async def get_feedback_list(org_id:int,
                            product_id:int,
                            current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("feedback.view"))],
                            feedback_service:Annotated[FeedBackService,Depends(get_service)])->ApiResponse[list[FeedbackRead]]:
    result=await feedback_service.get_feedback_list(org_id,product_id)
    return ApiResponse(success=True,data=result)

@router.post("/",response_model=ApiResponse[FeedbackRead])
async def create_feedback(org_id:int,
                          product_id:int,
                          feedback_create:FeedbackCreate,
                          current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("feedback.create"))],
                          feedback_service:Annotated[FeedBackService,Depends(get_service)])->ApiResponse[FeedbackRead]:
    result=await feedback_service.create_feedback(org_id,product_id,feedback_create,current_user)
    return ApiResponse(success=True,data=result)

@router.put("/{feedback_id}",response_model=ApiResponse[FeedbackRead])
async def update_feedback(org_id:int,
                          product_id:int,
                          feedback_id:int,
                          feedback_update:FeedbackUpdate,
                          current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("feedback.edit_own","feedback.edit_all"))],
                          feedback_service:Annotated[FeedBackService,Depends(get_service)]
)->ApiResponse[FeedbackRead]:
    result = await feedback_service.update_feedback(org_id,product_id,feedback_id,feedback_update,current_user)
    return ApiResponse(success=True,data=result)

@router.delete("/{feedback_id}",response_model=ApiResponse[str])
async def delete_feedback(org_id:int,
                          product_id:int,
                          feedback_id:int,
                          current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("feedback.delete_own","feedback.delete_all"))],
                          feedback_service:Annotated[FeedBackService,Depends(get_service)])->ApiResponse[str]:
    await feedback_service.delete_feedback(org_id,product_id,feedback_id,current_user)
    return ApiResponse(success=True,data="Deleted feedback successfully")

@router.patch("/{feedback_id}/status",response_model=ApiResponse[FeedbackRead])
async def change_the_status(org_id:int,
                          product_id:int,
                          feedback_id:int,
                          feedback_status_update:FeedbackStatusUpdate,
                          current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("feedback.change_status"))],
                          feedback_service:Annotated[FeedBackService,Depends(get_service)])->ApiResponse[FeedbackRead]:
    result= await feedback_service.update_status(org_id=org_id,
                                                 product_id=product_id,
                                                 feedback_id=feedback_id,
                                                 current_user=current_user,
                                                 feedback_status_update=feedback_status_update)
    return ApiResponse(success=True,data=result)

@router.post("/{feedback_id}/votes",response_model=ApiResponse[str])
async def upvote_feedback(org_id:int,
                          product_id:int,
                          feedback_id:int,
                          feedback_vote_create:FeedbackVoteCreate,
                          current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("vote.create","vote.revoke"))],
                          feedback_service:Annotated[FeedBackService,Depends(get_service)])->ApiResponse[str]:
    count=await feedback_service.upvote_feedback(org_id=org_id,
                                           product_id=product_id,
                                           feedback_id=feedback_id,
                                           feedback_vote_create=feedback_vote_create,
                                           current_user=current_user)
    return ApiResponse(success=True,data=count)

@router.get("/{feedback_id}/votes",response_model=ApiResponse[int])
async def count_votes_for_feedback(org_id:int,
                                   product_id:int,
                                   feedback_id:int,
                                   current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("vote.view_counts"))],
                                   feedback_service:Annotated[FeedBackService,Depends(get_service)])->ApiResponse[int]:
    result=await feedback_service.get_feedback_votes_counts(org_id=org_id,
                                                     product_id=product_id,
                                                     feedback_id=feedback_id)
    return ApiResponse(success=True,data=result)