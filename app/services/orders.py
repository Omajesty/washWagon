from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.order_item import OrderItem
from app.models.orders import Order
from app.models.price_list import PriceList
from app.models.user import User
from app.schemas.order import CreateOrder


def create_order(
    session: Session,
    customer: User,
    data: CreateOrder,
) -> Order:

    order = Order(
        customer_id=customer.id,
        total=0,
    )

    session.add(order)
    session.flush()

    total = 0

    for item_data in data.items:

        statement = select(PriceList).where(
            PriceList.garment == item_data.garment
        )

        price = session.exec(statement).first()

        if price is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No price found for {item_data.garment.value}",
            )

        item_total = price.unit_price * item_data.quantity

        order_item = OrderItem(
            order_id=order.id,
            price_list_id=price.id,
            garment=item_data.garment,
            quantity=item_data.quantity,
            unit_price=price.unit_price,
        )

        session.add(order_item)

        total += item_total

    order.total = total

    session.commit()
    session.refresh(order)

    return order