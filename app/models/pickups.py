from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.slots import Slot
    from app.models.orders import Order
    from app.models.status_history import StatusHistory
    from app.models.payment import Payment
    from app.models.user import User

class Pickup(SQLModel, table=True):

    __tablename__ = "pickups"

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", unique=True)

    slot_id: int = Field(foreign_key="slots.id")

    courier_id: int | None = Field(default=None, foreign_key="users.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    order: "Order" = Relationship(back_populates="pickup")

    slot: "Slot" = Relationship(back_populates = "pickups")
    
    courier: "User | None" = Relationship(
        back_populates="courier_pickups",
        sa_relationship_kwargs={
            "foreign_keys": "Pickup.courier_id"
        }
    )
    
    status_history: list["StatusHistory"] = Relationship(back_populates="pickup")
    payment: "Payment | None" = Relationship(back_populates="pickup")
    
