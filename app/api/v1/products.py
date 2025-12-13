from typing import Annotated, Optional
from fastapi import APIRouter,Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.db import get_session
from app.core.dep import require_org_permission
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.product import ProductCreate, ProductRead, ProductReadDetailed, ProductUpdate
from app.schemas.users import AuthenticatedUser
from app.service.product_service import ProductService
# {"code": "product.view", "description": "View products and product boards"},
# {"code": "product.create", "description": "Create new products"},
# {"code": "product.edit", "description": "Edit existing products"},
# {"code": "product.archive", "description": "Archive or unarchive products"},
# {"code": "product.delete", "description": "Permanently delete products"},

router=APIRouter(prefix="/orgs/{org_id}",tags=["Products"])
def get_service(session:Annotated[AsyncSession,Depends(get_session)]):
    return ProductService(session)

@router.get("/products/{product_id}",response_model=ApiResponse[ProductReadDetailed])
async def get_product_by_product_id(org_id:int,
                      product_id:int,
                      current_user:Annotated[AuthenticatedUser,Depends(require_org_permission('product.view'))],
                      product_service:Annotated[ProductService,Depends(get_service)])->ApiResponse[ProductRead]:
    result=await product_service.get_product_by_product_id(org_id,product_id)
    return ApiResponse(success=True,data=result)

@router.get("/products",response_model=ApiResponse[list[ProductRead]])
async def get_product_list_by_org_id(org_id:int,
                                    current_user:Annotated[AuthenticatedUser,Depends(require_org_permission("product.view"))],
                                    product_service:Annotated[ProductService,Depends(get_service)],
                                    page:int=Query(default=0,ge=0,le=100),
                                    limit:int=Query(default=20,ge=1,le=100),
                                    q:Optional[str]=Query(default=None,description="Search in title/description")
                                    )->ApiResponse[list[ProductRead]]:
    result=await product_service.get_product_list_by_org_id(org_id,page,limit,q)
    return ApiResponse(success=True,data=result)

@router.post("/products",response_model=ApiResponse[ProductRead])
async def create_product_by_org_id(org_id:int,
                                   product_create:ProductCreate,
                                   current_user:Annotated[AuthenticatedUser,Depends(require_org_permission('product.create'))],
                                   product_service:Annotated[ProductService,Depends(get_service)])->ApiResponse[ProductRead]:
    result=await product_service.create_product_by_org_id(org_id,product_create,current_user)
    return ApiResponse(success=True,data=result)

@router.put("/products/{product_id}",response_model=ApiResponse[ProductRead])
async def update_product_by_org_id(org_id:int,
                                   product_id:int,
                                   product_update:ProductUpdate,
                                   current_user:Annotated[AuthenticatedUser,Depends(require_org_permission('product.edit'))],
                                   product_service:Annotated[ProductService,Depends(get_service)])->ApiResponse[ProductRead]:
    result=await product_service.update_product_by_org_id(org_id,product_id,product_update)
    return ApiResponse(success=True,data=result)

@router.delete("/products/{product_id}",response_model=ApiResponse[str])
async def delete_product_by_org_id(org_id:int,
                                   product_id:int,
                                   current_user:Annotated[AuthenticatedUser,Depends(require_org_permission('product.delete'))],
                                   product_service:Annotated[ProductService,Depends(get_service)])->ApiResponse[str]:
    await product_service.delete_product_by_org_id(org_id,product_id)
    return ApiResponse(success=True,data="Deleted product successfully")

# #Assign person to the product 
# @router.post()