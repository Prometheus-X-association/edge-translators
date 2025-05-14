from typing import List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class StatusEnum(int, Enum):
    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1

class RoleEnum(str, Enum):
    ROLE_PROVIDER = "ROLE_PROVIDER"
    ROLE_ADMIN = "ROLE_ADMIN"

class User(BaseModel):
    username: str = Field(default="")
    email: EmailStr = Field(default="")
    active: bool = Field(default=True)
    password: str = Field(default="", min_length=8)
    role: RoleEnum = Field(default=RoleEnum.ROLE_PROVIDER)

    def __str__(self):
        return self.username

    # def is_active(self) -> bool:
    #     return self.status is StatusEnum.STATUS_ACTIVE