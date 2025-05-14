import jwt
from jwt.exceptions import InvalidTokenError
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from ..user.model import User
from ..user.service import UserService
from ..user.dependencies import UserServiceDep, UserRepositoryDep
from ..auth.service import AuthService
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
AuthGuardDep = Annotated[str, Depends(oauth2_scheme)]

def get_auth_service(user_service: UserServiceDep) -> AuthService:
    return AuthService(user_service)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(user_repository: UserRepositoryDep , token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload: dict[str, Any] = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user_service = UserService(user_repository)
    user = await user_service.find_user_by_username(username)
    if user is None:
        raise credentials_exception
    if not user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user

CurrentUserdep = Annotated[User, Depends(get_current_user)]

class RoleChecker:  
  def __init__(self, allowed_roles):  
    self.allowed_roles = allowed_roles  
  
  def __call__(self, current_user: CurrentUserdep):  
    if current_user.role.value in self.allowed_roles:  
      return True  
    raise HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED,   
        detail=f"You don't have enough permissions"
    ) 
  
CheckRoleAdminDep = Annotated[bool, Depends(RoleChecker(allowed_roles=["ROLE_ADMIN"]))]