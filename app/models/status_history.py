from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field
from .pickups import Status


if TYPE_CHECKING:
    from app.models.pickups import Pickups

class StatusHistory(SQLModel, table=True):

    __tablename__ = "Status History"

    id: int | None = Field(default=None, primary_key=True)
    pickup_id: int = Field(foreign_key="pickup.id")
    stage: Status
    cereated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    pickups: "Pickups" = Relationship(back_populates="status_history")