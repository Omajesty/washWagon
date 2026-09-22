from typing import Optional

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.slots import Slot
    from app.models.user import User


class Zone(SQLModel, table=True):
    __tablename__ = "zones"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    slots: list["Slot"] = Relationship(back_populates="zone")
    users: list["User"] = Relationship(back_populates="zone")
