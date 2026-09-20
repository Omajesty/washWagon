from datetime import datetime, timezone
from enum import Enum

from sqlmodel import SQLModel, Field


class OrderStatus(str, Enum):
    BOOKED = "booked"
    COLLECTED = "collected"
    WASHING = "washing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def is_terminal(self) -> bool:
        return self in (
            OrderStatus.DELIVERED,
            OrderStatus.CANCELLED,
        )

    def can_transition_to(
        self,
        next_status: "OrderStatus",
    ) -> bool:
        transitions = {
            OrderStatus.BOOKED: (
                OrderStatus.COLLECTED,
                OrderStatus.CANCELLED,
            ),
            OrderStatus.COLLECTED: (
                OrderStatus.WASHING,
                OrderStatus.CANCELLED,
            ),
            OrderStatus.WASHING: (
                OrderStatus.READY,
                OrderStatus.CANCELLED,
            ),
            OrderStatus.READY: (
                OrderStatus.OUT_FOR_DELIVERY,
                OrderStatus.CANCELLED,
            ),
            OrderStatus.OUT_FOR_DELIVERY: (
                OrderStatus.DELIVERED,
                OrderStatus.CANCELLED,
            ),
            OrderStatus.DELIVERED: (),
            OrderStatus.CANCELLED: (),
        }

        return next_status in transitions[self]


class Order(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    customer_id: int = Field(
        foreign_key="user.id"
    )

    total: int = Field(
        default=0,
        ge=0,
    )

    status: OrderStatus = OrderStatus.BOOKED

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )