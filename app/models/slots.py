from datetime import time, date

from sqlmodel import SQLModel, Field


class Slots(SQLModel, table=True):
    id: int
    zone_id: int
    capacity: int = 5
    booked_count: int
    date: date
    start_at: time
    stop_at: time


    