from sqlmodel import SQLModel, Field
from app.schemas.order import GarmentType

class PriceList(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    garment: GarmentType
    unit_price: int = Field(gt=0)