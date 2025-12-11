from typing import Annotated
from fastapi import APIRouter, Depends

from app.core.db import get_session
from app.core.dep import require_org_permission
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.schemas.common import ApiResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.users import AuthenticatedUser
from app.service.comment_service import CommentService
def get_service(session:AsyncSession=Depends(get_session)):
    return CommentService(session)
# {"code": "comment.view", "description": "View comments"},
# {"code": "comment.create", "description": "Add comments"},
# {"code": "comment.edit_own", "description": "Edit own comments"},
# {"code": "comment.delete_own", "description": "Delete own comments"},
# {"code": "comment.moderate", "description": "Moderate any comment"},

router=APIRouter(prefix="/orgs/{org_id}/products/{product_id}/feedback/{feedback_id}/comment",tags=["Comment"])


@router.get("/{comment_id}", response_model=ApiResponse[CommentRead])
async def get_comment_by_id(
    org_id: int,
    product_id: int,
    feedback_id: int,
    comment_id: int,
    current_user: Annotated[
        AuthenticatedUser,
        Depends(require_org_permission("comment.view"))
    ],
    comment_service: Annotated[CommentService, Depends(get_service)],
) -> ApiResponse[CommentRead]:
    result = await comment_service.get_comment_by_id(
        org_id=org_id,
        product_id=product_id,
        feedback_id=feedback_id,
        comment_id=comment_id,
    )
    return ApiResponse(success=True, data=result)


@router.get("/", response_model=ApiResponse[list[CommentRead]])
async def get_comment_list(
    org_id: int,
    product_id: int,
    feedback_id: int,
    current_user: Annotated[
        AuthenticatedUser,
        Depends(require_org_permission("comment.view"))
    ],
    comment_service: Annotated[CommentService, Depends(get_service)],
) -> ApiResponse[list[CommentRead]]:
    result = await comment_service.get_comment_list(
        org_id=org_id,
        product_id=product_id,
        feedback_id=feedback_id,
    )
    return ApiResponse(success=True, data=result)


@router.post("/", response_model=ApiResponse[CommentRead])
async def create_comment(
    org_id: int,
    product_id: int,
    feedback_id: int,
    comment_create: CommentCreate,
    current_user: Annotated[
        AuthenticatedUser,
        Depends(require_org_permission("comment.create"))
    ],
    comment_service: Annotated[CommentService, Depends(get_service)],
) -> ApiResponse[CommentRead]:
    result = await comment_service.create_comment(
        org_id=org_id,
        product_id=product_id,
        feedback_id=feedback_id,
        comment_create=comment_create,
        current_user=current_user,
    )
    return ApiResponse(success=True, data=result)


@router.put("/{comment_id}", response_model=ApiResponse[CommentRead])
async def update_comment(
    org_id: int,
    product_id: int,
    feedback_id: int,
    comment_id: int,
    comment_update: CommentUpdate,
    current_user: Annotated[
        AuthenticatedUser,
        Depends(require_org_permission("comment.edit_own", "comment.moderate"))
    ],
    comment_service: Annotated[CommentService, Depends(get_service)],
) -> ApiResponse[CommentRead]:
    result = await comment_service.update_comment(
        org_id=org_id,
        product_id=product_id,
        feedback_id=feedback_id,
        comment_id=comment_id,
        comment_update=comment_update,
        current_user=current_user,
    )
    return ApiResponse(success=True, data=result)


@router.delete("/{comment_id}", response_model=ApiResponse[str])
async def delete_comment(
    org_id: int,
    product_id: int,
    feedback_id: int,
    comment_id: int,
    current_user: Annotated[
        AuthenticatedUser,
        Depends(require_org_permission("comment.delete_own", "comment.moderate"))
    ],
    comment_service: Annotated[CommentService, Depends(get_service)],
) -> ApiResponse[str]:
    await comment_service.delete_comment(
        org_id=org_id,
        product_id=product_id,
        feedback_id=feedback_id,
        comment_id=comment_id,
        current_user=current_user,
    )
    return ApiResponse(success=True, data="Deleted comment successfully")

