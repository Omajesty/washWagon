from sqlmodel import SQLModel, Field


class Order_items(SQLModel, table=True):
    id: int
    pickup_id: int
    garment: str
    quantity: int
    unit_price: int