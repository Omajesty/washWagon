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