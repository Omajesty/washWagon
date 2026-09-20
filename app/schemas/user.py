from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    OPS_MANAGER = "ops_manager"
    COURIER = "courier"
    CUSTOMER = "customer"


class User(BaseModel):
    name: str = Field(max_length=125)
    email: EmailStr


class UserRegister(User):
    zone: str = Field(min_length=1, max_length=25)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(User):
    id: int
    role: Role = Role.CUSTOMER
