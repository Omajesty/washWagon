from enum import Enum

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class Role(str, Enum):
    OPS_MANAGER = "ops_manager"
    COURIER = "courier"
    CUSTOMER = "customer"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    hashed_password: str
    role: Role = Role.CUSTOMER
    zone_id: int = Field(foreign_key="zone.id")
