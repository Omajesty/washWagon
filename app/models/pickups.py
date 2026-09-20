from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime, timezone


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
    id: int | None = Field(default=None, primary_key=True)    
    slot_id: int = Field(foreign_key="slot.id")
    user_id: int = Field(foreign_key="user.id")
    courier_id: int | None = Field(
        default=None,
        foreign_key="user.id"
    )
    total: int = Field(default=0, ge=0)
    status: Status = Status.BOOKED

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
