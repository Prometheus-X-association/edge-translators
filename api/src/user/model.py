from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from enum import Enum

class StatusEnum(int, Enum):
    ACTIVE = 1
    INACTIVE = 0

class RoleEnum(str, Enum):
    ROLE_PROVIDER = "ROLE_PROVIDER"
    ROLE_ADMIN = "ROLE_ADMIN"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    email: str = Field(index=True, nullable=False, unique=True)
    status: StatusEnum = Field(default=StatusEnum.ACTIVE, nullable=False)
    password: str = Field(nullable=False)
    role: RoleEnum = Field(default=RoleEnum.ROLE_PROVIDER, nullable=False)
    logged_in: bool = Field(default=False, nullable=False)
    failed_login_attempts: int = Field(default=0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    def __str__(self) -> str:
        return self.username

class UserResponse(BaseModel):
    id: Optional[int]
    username: str
    email: str
    status: StatusEnum
    role: RoleEnum
    logged_in: bool
    failed_login_attempts: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
