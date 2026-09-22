from typing import Optional

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.orders import Order
    from app.models.pickups import Pickup
    from app.models.zones import Zone


class Role(str, Enum):
    OPS_MANAGER = "ops_manager"
    COURIER = "courier"
    CUSTOMER = "customer"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    role: Role = Field(default=Role.CUSTOMER)
    zone_id: Optional[int] = Field(default=None, foreign_key="zones.id")

    zone: Optional["Zone"] = Relationship(back_populates="users")
    orders: list["Order"] = Relationship(back_populates="customer")
    courier_pickups: list["Pickup"] = Relationship(
        back_populates="courier",
        sa_relationship_kwargs={"foreign_keys": "Pickup.courier_id"},
    )
