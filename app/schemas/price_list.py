from pydantic import BaseModel, Field

from app.schemas.order import GarmentType


class CreatePrice(BaseModel):
    garment: GarmentType
    unit_price: int = Field(gt=0)


class UpdatePrice(BaseModel):
    unit_price: int = Field(gt=0)


class PriceOut(BaseModel):
    id: int
    garment: GarmentType
    unit_price: int