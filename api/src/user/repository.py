from typing import Sequence
from sqlmodel import select
from .model import User
from ..database import SessionDep

class UserRepository:
    
    def __init__(self, db: SessionDep) -> None:
        self.db = db

    def find(self, id: int) -> User | None:
        user = self.db.get(User, id)
        return user

    def find_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        user = self.db.exec(statement).first()
        return user

    def find_all(self, page: int, per_page: int, sort: str, order: str) -> tuple[int, Sequence[User]]:
        statement = select(User)

        offset = (page - 1) * per_page
        if order == "DESC":
            statement = statement.order_by(getattr(User, sort).desc())
        else:
            statement = statement.order_by(getattr(User, sort).asc())

        total_users = len(self.db.exec(statement).all())

        users = self.db.exec(statement.offset(offset).limit(per_page)).all()

        return total_users, users

    def create(self, new_user: User) -> User:
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def update(self, user_to_update: User) -> User:
        if not user_to_update.id:
            raise Exception("error during user update.")
        user_in_db = self.find(user_to_update.id)
        if not user_in_db:
            raise Exception("error during user update.")

        update_data = user_to_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user_in_db, key, value)
        
        self.db.add(user_in_db)
        self.db.commit()
        self.db.refresh(user_in_db)
        
        return user_in_db

    def delete(self, user: User) -> None:        
        self.db.delete(user)
        self.db.commit()