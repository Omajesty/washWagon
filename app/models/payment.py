from enum import Enum

from sqlmodel import SQLModel, Field


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class Payment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    pickup_id: int = Field(foreign_key="pickup.id")

    amount: int = Field(gt=0)

    status: PaymentStatus = PaymentStatus.PENDING

    reference: str