from enum import Enum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.zones import Zone
    from app.models.orders import Order
    from app.models.pickups import Pickup


class Role(str, Enum):
    OPS_MANAGER = "ops_manager"
    COURIER = "courier"
    CUSTOMER = "customer"


class User(SQLModel, table=True):

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    hashed_password: str
    role: Role = Field(default=Role.CUSTOMER)

    zone_id: int | None = Field(
        default=None,
        foreign_key="zones.id"
        )

    zone: "Zone | None" = Relationship(back_populates="users")

    ordes: list["Order"] = Relationship(
        back_populates="customer")

    courier_pickups: list["Pickup"] = Relationship(
        back_populates="courier",
        sa_relationship_kwargs={
            "foreign_keys": "Pickup.courier_id"
        }
    )