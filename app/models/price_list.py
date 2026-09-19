from sqlmodel import SQLModel, Field


class PriceList(SQLModel, table=True):
    id: int
    garment: str
    unit_price: int