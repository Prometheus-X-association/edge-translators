from typing import Literal, Sequence, TypedDict
from fastapi import Body, HTTPException, Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import Response
from fastapi.param_functions import Path

from .dependencies import UserServiceDep
from .model import User, UserCreate
from ..auth.dependencies import CurrentUserdep, CheckRoleAdminDep


router = InferringRouter(tags=['user'])

class SortParams(TypedDict):
    field: Literal["id", "username", "email", "roles"]
    order: Literal["ASC", "DESC"]

@cbv(router)
class UserController:
    def __init__(self, current_user: CurrentUserdep, user_service: UserServiceDep) -> None:
        self.current_user = current_user
        self.user_service = user_service
    
    @router.get("/users/me", response_model=User)
    async def get_me(self) -> User:
        return self.current_user

    @router.get("/users/{id}", response_model=User, description="Get a User")
    async def get_user(self, _: CheckRoleAdminDep, id: int = Path()) -> User:
        user = await self.user_service.find_user(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    @router.get("/users", response_model=Sequence[User], description="Get Users filtered, ordered and paginated")
    async def get_users(
        self,
        response: Response,
        _: CheckRoleAdminDep,
        # filter: Optional[str] = Query("{}", alias="filter"),
        page: int = Query(1, alias="page"),
        per_page: int = Query(5, alias="per_page"),
        sort: Literal["id", "username", "email", "created_at", "updated_at", "deleted_at"] = Query('id', alias="sort"),
        order: Literal["ASC", "DESC"] = Query('ASC', alias="order"),
    ) -> Sequence[User]:
        total_users, users = await self.user_service.find_users(page, per_page, sort, order)

        response.headers["Content-Range"] = f"users 0-{total_users-1}/{total_users}"
        
        return users

    @router.post("/users", description="Create a User")
    async def create_user(self, user: UserCreate = Body(...)) -> User: 
        return await self.user_service.create_user(user)
    
    @router.patch("/users/{id}", description="Update a User")
    async def patch_user(self, user: User = Body(...)) -> User: 
        return await self.user_service.update_user(user)

    @router.put("/users/{id}", description="Update a User")
    async def put_user(self, user: User = Body(...)) -> User:
        return await self.user_service.update_user(user)

    @router.delete("/users/{id}", description="Delete a User")
    async def delete_user(self, _: CheckRoleAdminDep, id: int = Path()) -> bool:
        await self.user_service.delete_user(id)
        return True