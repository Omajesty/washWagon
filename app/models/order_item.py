from sqlmodel import SQLModel, Field

from app.schemas.order import GarmentType


<<<<<<< HEAD
class OrderItems(SQLModel, table=True):

    __tablename__ = "Order Items"

=======
class OrderItem(SQLModel, table=True):
>>>>>>> 80e6c1a7af9f4da3126292be6a0e92e02cb1bdd5
    id: int | None = Field(default=None, primary_key=True)    
    order_id: int = Field(foreign_key="order.id")
    price_list_id: int = Field(foreign_key="price_list.id")
    garment: GarmentType
    quantity: int = Field(gt=0)
    unit_price: int = Field(gt=0)