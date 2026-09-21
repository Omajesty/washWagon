from pydantic import BaseModel, Field

from enum import Enum


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