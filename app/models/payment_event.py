from typing import Optional

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class PaymentEvent(SQLModel, table=True):
    """Stores webhook event IDs so provider retries are processed once."""

    __tablename__ = "payment_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(unique=True, index=True)
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
