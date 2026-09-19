from sqlmodel import SQLModel, Field
from enum import Enum


# class Status(str, Enum):
#     BOOKED = "booked"
#     COLLECTED = "collected"
#     WASHING = "washing" 
#     READY = "ready"
#     OUT_FOR_DELIVERY = "out_for_delievery"
#     DELIVERED = "delivered"

class Status(str, Enum):
    """Concrete pickup lifecycle status with transition behavior."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
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
            Status.PENDING: (Status.ACCEPTED, Status.CANCELLED),
            Status.ACCEPTED: (Status.PICKED_UP, Status.CANCELLED),
            Status.PICKED_UP: (Status.IN_TRANSIT, Status.CANCELLED),
            Status.IN_TRANSIT: (Status.DELIVERED, Status.CANCELLED),
            Status.DELIVERED: (),
            Status.CANCELLED: (),
        }
        return next_status in transitions[self]


class Pickups(SQLModel, table=True):
    id: int
    slot_id: int
    user_id: int
    courier_id: int
    total: int
    status: Status
