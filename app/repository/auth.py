from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.organization_membership import OrganizationMembership
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission

async def user_has_org_permission(org_id:int,user_id:int,session:AsyncSession,permission_code:str)->bool:
    stmt=(select(Permission.id)
            .join(RolePermission,Permission.id==RolePermission.permission_id)
            .join(Role,Role.id==RolePermission.role_id)
            .join(OrganizationMembership,OrganizationMembership.role_id==Role.id)
            .where(
                OrganizationMembership.user_id==user_id,
                OrganizationMembership.org_id==org_id,
                Permission.code==permission_code
            )
            .limit(1)
    )
    result = await session.exec(stmt)
    return result.first() is not None

