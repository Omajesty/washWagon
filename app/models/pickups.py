from typing import TYPE_CHECKING

from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.slots import Slot
    from app.models.order_item import OrderItems
    from app.models.status_history import StatusHistory
    from app.models.payment import Payment
    from app.models.user import User


# class Status(str, Enum):
#     BOOKED = "booked"
#     COLLECTED = "collected"
#     WASHING = "washing" 
#     READY = "ready"
#     OUT_FOR_DELIVERY = "out_for_delievery"
#     OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"

class PickupStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    COLLECTED = "collected"
    CANCELLED = "cancelled"

    def is_terminal(self) -> bool:
        return self in (
            PickupStatus.COLLECTED,
            PickupStatus.CANCELLED,
        )

    def can_transition_to(
        self,
        next_status: "PickupStatus",
    ) -> bool:
        transitions = {
            PickupStatus.PENDING: (
                PickupStatus.ACCEPTED,
                PickupStatus.CANCELLED,
            ),
            PickupStatus.ACCEPTED: (
                PickupStatus.COLLECTED,
                PickupStatus.CANCELLED,
            ),
            PickupStatus.COLLECTED: (),
            PickupStatus.CANCELLED: (),
        }

        return next_status in transitions[self]


class Pickup(SQLModel, table=True):

    __tablename__ = "Pickups"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    # One order can have only one pickup
    order_id: int = Field(
        foreign_key="order.id",
        unique=True,
    )

    slot_id: int = Field(
        foreign_key="slot.id"
    )

    courier_id: int | None = Field(
        default=None,
        foreign_key="user.id",
    )

    status: PickupStatus = PickupStatus.PENDING

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    slot: "Slot" = Relationship(back_populates = "pickups")
    order_item: list["OrderItems"] = Relationship(back_populates="pickup")
    status_history: list["StatusHistory"] = Relationship(back_populates="pickup")
    payment: "Payment" = Relationship(back_populates="pickups")

    customer: "User" = Relationship(
        back_populates="customer_pickups",
        sa_relationship_kwargs={
            "foreign_keys": "Pickup.user_id"
        }
    )

    courier: "User" | None = Relationship(
        back_populates="courier_pickups",
        sa_relationship_kwargs={
            "foreign_keys": "Pickup.courier_id"
        }
    )