from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import ConflictException, NotFoundException
from app.models import organization
from app.models.products import Product
from app.repository.product_repository import ProductRepository
from app.schemas.organization import OrganizationOut
from app.schemas.product import ProductCreate, ProductRead, ProductReadDetailed, ProductUpdate
from app.schemas.users import AuthenticatedUser, UserOut
class ProductService:
    def __init__(self,session:AsyncSession):
        self.repo=ProductRepository(session)
    async def get_product_by_product_id(self,org_id:int,product_id:int)->ProductReadDetailed:
        
        product=await self.repo.get_detail_product_by_product_id(org_id,product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Invalid product or org_id ")
        print(product)
        product_read_detail=ProductReadDetailed(**product.model_dump(exclude=["organization","created_by_user"]),
                                                organization=OrganizationOut.model_validate(product.organization),
                                                created_by_user=UserOut.model_validate(product.created_by_user))
        return product_read_detail
    
    async def get_product_list_by_org_id(self,org_id:int,page:int,limit:int,q:str)->list[ProductRead]:
        product_list=await self.repo.get_product_list_by_org_id(org_id,page,limit,q)
        product_read=[ProductRead.model_validate(product) for product in product_list]
        return product_read
        
    async def create_product_by_org_id(self,org_id:int,product_create:ProductCreate,current_user:AuthenticatedUser)->ProductRead:
        product=Product(**product_create.model_dump(),org_id=org_id,created_by=current_user.id)
        try:
            product_created=await self.repo.save(product)
        except IntegrityError as e:
            raise ConflictException(
                message="Product name already exists",
                details="A product with this name already exists in this organization",
            )
        return ProductRead.model_validate(product_created)

    async def update_product_by_org_id(self,org_id:int,product_id:int,product_update:ProductUpdate)->ProductRead:
        product=await self.repo.get_product_by_product_id(org_id,product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Invalid product or org_id ")
        for key,value in product_update.model_dump(exclude_unset=True).items():
            setattr(product,key,value)
        try:
            product_updated=await self.repo.save(product)
        except IntegrityError as e:
            raise ConflictException(
                message="Product name already exists",
                details="A product with this name already exists in this organization",
            )
        return ProductRead.model_validate(product_updated)

    async def delete_product_by_org_id(self,org_id:int,product_id:int)->None:
        product=await self.repo.get_product_by_product_id(org_id,product_id)
        if not product:
            raise NotFoundException(message="Product Not Found",details="Invalid product or org_id ")
        await self.repo.delete(product)

        
