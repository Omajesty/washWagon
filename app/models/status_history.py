from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field


if TYPE_CHECKING:
    from app.models.pickups import Pickup
    from app.models.orders import OrderStatus


class StatusHistory(SQLModel, table=True):

    __tablename__ = "status_history"

    id: int | None = Field(default=None, primary_key=True)
    pickup_id: int = Field(foreign_key="pickups.id")
    stage: OrderStatus
    cereated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    pickups: "Pickup" = Relationship(back_populates="status_history")