from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User

if TYPE_CHECKING:
    from app.models.slots import Slot
class Zone(SQLModel, table=True):

    __tablename__ = "Zones"

    id: int | None = Field(default=None, primary_key=True)
    name: str

    slots: list["Slot"] = Relationship(back_populates="zone")
    users: list["User"] = Relationship(back_populates="zone")