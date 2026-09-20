from sqlmodel import SQLModel, Field

from app.schemas.order import GarmentType


class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)    
    order_id: int = Field(foreign_key="order.id")
    price_list_id: int = Field(foreign_key="price_list.id")
    garment: GarmentType
    quantity: int = Field(gt=0)
    unit_price: int = Field(gt=0)