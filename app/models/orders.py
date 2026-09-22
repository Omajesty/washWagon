from typing import Optional

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.order_item import OrderItem
    from app.models.pickups import Pickup
    from app.models.user import User


class OrderStatus(str, Enum):
    BOOKED = "booked"
    COLLECTED = "collected"
    WASHING = "washing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    def is_terminal(self) -> bool:
        return self in (OrderStatus.DELIVERED, OrderStatus.CANCELLED)

    def can_transition_to(self, next_status: OrderStatus) -> bool:
        transitions = {
            OrderStatus.BOOKED: (OrderStatus.COLLECTED, OrderStatus.CANCELLED),
            OrderStatus.COLLECTED: (OrderStatus.WASHING, OrderStatus.CANCELLED),
            OrderStatus.WASHING: (OrderStatus.READY, OrderStatus.CANCELLED),
            OrderStatus.READY: (OrderStatus.OUT_FOR_DELIVERY, OrderStatus.CANCELLED),
            OrderStatus.OUT_FOR_DELIVERY: (OrderStatus.DELIVERED, OrderStatus.CANCELLED),
            OrderStatus.DELIVERED: (),
            OrderStatus.CANCELLED: (),
        }
        return next_status in transitions[self]


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="users.id")
    total: int = Field(default=0, ge=0)
    status: OrderStatus = Field(default=OrderStatus.BOOKED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    customer: "User" = Relationship(back_populates="orders")
    items: list["OrderItem"] = Relationship(back_populates="order")
    pickup: Optional["Pickup"] = Relationship(back_populates="order")
