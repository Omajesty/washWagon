from typing import Optional

from datetime import date, time
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.pickups import Pickup
    from app.models.zones import Zone


class Slot(SQLModel, table=True):
    __tablename__ = "slots"

    id: Optional[int] = Field(default=None, primary_key=True)
    zone_id: int = Field(foreign_key="zones.id")
    capacity: int = Field(default=5, gt=0)
    booked_count: int = Field(default=0, ge=0)
    date: date
    start_at: time
    stop_at: time

    zone: "Zone" = Relationship(back_populates="slots")
    pickups: list["Pickup"] = Relationship(back_populates="slot")
