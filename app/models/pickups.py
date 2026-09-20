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

class Status(str, Enum):
    """Concrete pickup lifecycle status with transition behavior."""

    BOOKED = "booked"
    COLLECTED = "collected"
    WASHING = "washing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def __str__(self) -> str:
        return self.value

    def is_terminal(self) -> bool:
        """Return whether this status ends the pickup lifecycle."""
        return self in (Status.DELIVERED, Status.CANCELLED)

    def can_transition_to(self, next_status: "Status") -> bool:
        """Return whether a direct transition to ``next_status`` is valid."""
        transitions = {
            Status.BOOKED: (Status.COLLECTED, Status.CANCELLED),
            Status.COLLECTED: (Status.WASHING, Status.CANCELLED),
            Status.WASHING: (Status.READY, Status.CANCELLED),
            Status.READY: (Status.OUT_FOR_DELIVERY, Status.CANCELLED),
            Status.OUT_FOR_DELIVERY: (Status.DELIVERED, Status.CANCELLED),
            Status.DELIVERED: (),
            Status.CANCELLED: (),
        }
        return next_status in transitions[self]


class Pickups(SQLModel, table=True):

    __tablename__ = "Pickups"

    id: int | None = Field(default=None, primary_key=True)    
    slot_id: int = Field(foreign_key="slot.id")
    user_id: int = Field(foreign_key="user.id")
    courier_id: int | None = Field(
        default=None,
        foreign_key="user.id",
        index=True
    )
    total: int = Field(default=0, ge=0)
    status: Status = Field(default=Status.BOOKED, index=True)

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