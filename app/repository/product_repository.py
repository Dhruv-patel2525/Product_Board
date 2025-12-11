from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.products import Product
from sqlalchemy.orm import selectinload
class ProductRepository:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def get_product_by_product_id(self,org_id:int,product_id:int)->Optional[Product]:
        stmt=select(Product).where(Product.id==product_id,Product.org_id==org_id)
        result=await self.session.exec(stmt)
        return result.one_or_none()
    async def get_detail_product_by_product_id(self,org_id:int,product_id:int)->Optional[Product]:
        stmt=select(Product).where(Product.id==product_id,Product.org_id==org_id).options(selectinload(Product.organization),selectinload(Product.created_by_user))
        result=await self.session.exec(stmt)
        return result.one_or_none()
    async def get_product_list_by_org_id(self,org_id:int)->list[Product]:
        stmt=select(Product).where(Product.org_id==org_id)
        result=await self.session.exec(stmt)
        return result.all()
    async def save(self,product:Product)->Product:
        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)
        return product
    async def delete(self,product:Product)->None:
        await self.session.delete(product)
        await self.session.flush()