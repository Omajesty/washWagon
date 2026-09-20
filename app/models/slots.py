from datetime import time, date

from sqlmodel import SQLModel, Field


class Slot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    zone_id: int = Field(foreign_key="zone.id")
    capacity: int = Field(default=5, gt=0)
    booked_count: int =Field(default=0, ge=0)
    date: date
    start_at: time
    stop_at: time
    


    