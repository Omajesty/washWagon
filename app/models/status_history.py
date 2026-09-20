from sqlmodel import SQLModel, Field
from .pickups import Status


class StatusHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pickup_id: int = Field(foreign_key="pickup.id")
    stage: Status
