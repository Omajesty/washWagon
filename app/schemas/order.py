from pydantic import BaseModel, Field

from enum import Enum
from datetime import datetime


class GarmentType(str, Enum):
    SHIRT = "shirt"
    JEAN = "jean"
    JOGGER = "jogger"
    DRESS = "dress"
    SKIRT = "skirt"
    JACKET = "jacket"
    SWEATER = "sweater"
    SHOES = "shoes"

class CreateOrderItem(BaseModel):
    garment: GarmentType
    quantity: int = Field(gt=0)


class CreateOrder(BaseModel):
    items: list[CreateOrderItem] = Field(min_length=1)

class OrderItemOut(BaseModel):
    id: int
    garment: GarmentType
    quantity: int
    unit_price: int


class OrderOut(BaseModel):
    id: int
    customer_id: int
    total: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]