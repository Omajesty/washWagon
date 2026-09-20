from enum import Enum
from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.pickups import Pickups


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class Payment(SQLModel, table=True):

    __tablename__ = "Payments"

    id: int | None = Field(default=None, primary_key=True)

    pickup_id: int = Field(
        foreign_key="pickup.id",
        unique=True
        )

    amount: int = Field(gt=0)

    status: PaymentStatus = PaymentStatus.PENDING

    reference: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    pickup: "Pickups" = Relationship(back_populates="payment")