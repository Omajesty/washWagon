from typing import Optional

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.pickups import Pickup


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    pickup_id: int = Field(foreign_key="pickups.id", unique=True)
    amount: int = Field(gt=0)
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    reference: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    pickup: "Pickup" = Relationship(back_populates="payment")
