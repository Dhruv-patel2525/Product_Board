from unittest.mock import AsyncMock, create_autospec, patch
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.users import UserCreate, UserOut
from app.service.user_service import UserService
"""
1. create_user
    if user exists raise ConflictException is raised
    password is hashed before saving 
    saving function is called 
    background task for register_email should be called
    function should return the output in UserOut schema
2. login
    if user not exists raise NotFound Exception
    if user is not active return UnAuthorized Exception
    verify_password function is called to check password is equal  and compares the password
    create_access_token function is called to generate the JWT token
    output should be returend in UserOut schema

3. update_user
    if check user-id from the token and url if it is mismatch return Conflict Exception
    if user not exists raise NotFound Exception
    update/save function is called properly
    Output return in userOut schema
    only provides field updated

4. delete_user
    if check user-id from the token and url if it is mismatch return Conflict Exception
    if user not exists raise NotFound Exception
    delete function is called 

"""
def make_service_with_mock_repo():
    session_mock=AsyncMock(spec=AsyncSession)
    service=UserService(session_mock)
    mock_repo=create_autospec(UserRepository,instance=True,spec_set=True)
    service.repo=mock_repo
    return service,mock_repo
@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_user_success_with_mock_repo():
    service,repo=make_service_with_mock_repo()
    user_in=UserCreate(name="John",username="john@email.com",password="somethingunique")
    repo.getUserByUserName=AsyncMock(return_value=None)
    repo.save=AsyncMock(return_value=User(
        id=1,
        name="John",
        username="john@email.com",
        password_hash="HASHED",
        is_active=True,
    ))
    with patch("app.service.user_service.hash_password", return_value="HASHED") as mock_hash, \
         patch("app.service.user_service.send_welcome_email") as mock_email:
        result=await service.create_user(user_in)
        repo.getUserByUserName.assert_awaited_once_with(username="john@email.com")
        repo.save.assert_awaited_once()
        mock_hash.assert_called_once_with("somethingunique")
        mock_email.delay.assert_called_once_with(email="john@email.com",full_name="John")
        assert isinstance(result,UserOut)
        assert result.id==1
        assert result.username=="john@email.com"




