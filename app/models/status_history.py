from typing import Optional

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.orders import OrderStatus

if TYPE_CHECKING:
    from app.models.pickups import Pickup


class StatusHistory(SQLModel, table=True):
    __tablename__ = "status_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    pickup_id: int = Field(foreign_key="pickups.id")
    stage: OrderStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    pickup: "Pickup" = Relationship(back_populates="status_history")
