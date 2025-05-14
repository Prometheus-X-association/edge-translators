import bcrypt
from typing import Sequence
from fastapi import HTTPException
from .model import User, UserCreate
from .repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    async def find_user(self, id: int) -> User | None:
        return self.user_repository.find(id)

    async def find_user_by_username(self, username: str) -> User | None:
        return self.user_repository.find_by_username(username)

    async def find_users(self, page: int = 1, per_page: int = 10, sort: str = "id", order: str = 'ASC') -> tuple[int, Sequence[User]]:
        total_users, users = self.user_repository.find_all(page, per_page, sort, order)
        return total_users, users
    
    async def create_user(self, payload: UserCreate) -> User:
        payload.password = self.get_password_hash(payload.password)
        user_to_create = User(**payload.dict())
        created_user = self.user_repository.create(user_to_create)
        
        return created_user
    
    async def update_user(self, payload: User) -> User:

        has_password_changed = False
        if payload.id:
            user = await self.find_user(payload.id)
            if user:
                has_password_changed = payload.password != user.password

        if has_password_changed:
            payload.password = self.get_password_hash(payload.password)
        user_to_update = User(**payload.dict())
        updated_user = self.user_repository.update(user_to_update)
        
        return updated_user

    async def delete_user(self, id: int) -> None:
        user = self.user_repository.find(id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return self.user_repository.delete(user)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    @staticmethod
    def get_password_hash(password) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()
    
