from sqlmodel import SQLModel, Field

from app.schemas.order import GarmentType


class Order_items(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)    
    pickup_id: int = Field(foreign_key="pickup.id")
    garment: GarmentType
    quantity: int = Field(gt=0)
    unit_price: int = Field(gt=0)