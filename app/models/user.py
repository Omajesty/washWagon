from enum import Enum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.zones import Zone
    from app.models.pickups import Pickups


class Role(str, Enum):
    OPS_MANAGER = "ops_manager"
    COURIER = "courier"
    CUSTOMER = "customer"


class User(SQLModel, table=True):

    __tablename__ = "Users"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    hashed_password: str
    role: Role = Role.CUSTOMER

    zone_id: int = Field(
        default=None,
        foreign_key="zone.id"
        )

    zone: "Zone" | None = Relationship(back_populates="user")

    customer_pickups: list["Pickups"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={
            "foreign_keys": "Pickup.user_id"
        }
    )

    courier_pickups: list["Pickups"] = Relationship(
        back_populates="courier",
        sa_relationship_kwargs={
            "foreign_keys": "Pickup.courier_id"
        }
    )