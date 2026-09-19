
from sqlmodel import SQLModel, Field
from pickups import Status



class StatusHistory(SQLModel, table=True):
    id: int
    pickup_id: int
    stage: Status