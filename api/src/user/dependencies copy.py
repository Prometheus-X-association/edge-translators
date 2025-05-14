from fastapi import Depends
from typing_extensions import Annotated
from .service import UserService
from .repository import UserRepository
from ..database import SessionDep

async def get_user_repository(db: SessionDep) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

async def get_user_service(user_repository: UserRepositoryDep) -> UserService:
    return UserService(user_repository)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

