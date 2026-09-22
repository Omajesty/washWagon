from typing import Optional

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.schemas.order import GarmentType

if TYPE_CHECKING:
    from app.models.orders import Order
    from app.models.price_list import PriceList


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    price_list_id: int = Field(foreign_key="price_list.id")
    garment: GarmentType
    quantity: int = Field(gt=0)
    unit_price: int = Field(gt=0)

    order: "Order" = Relationship(back_populates="items")
    price_list: "PriceList" = Relationship()
