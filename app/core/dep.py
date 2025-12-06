from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import jwt

from app.core.db import get_session
# from app.models import user
from app.models.user import User
from app.core.config import get_settings
from app.models.role import Role
from app.repository.auth import user_has_org_permission
from app.service.organization_service import OrganizationService

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/user/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        user_id = int(sub)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        # any other token error (bad signature, malformed, etc.)
        raise credentials_exception

    # fetch user from DB
    result = await session.exec(select(User).where(User.id == user_id))
    user = result.first()

    if not user or not user.is_active:
        raise credentials_exception

    return user


def require_roles(*allowed_roles: Role):
    async def _wrapper(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return _wrapper


def require_org_permission(permission_code:str):
    async def dependency(id:int,
                         current_user:User=Depends(get_current_user),
                         session:AsyncSession=Depends(get_session))->None:
        
        has_perm=await user_has_org_permission(
            org_id=id,
            user_id=current_user.id,
            session=session,
            permission_code=permission_code,
        )
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not Authorized for these org"
            ) 
        return current_user
    return dependency

