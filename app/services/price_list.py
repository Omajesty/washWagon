from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.price_list import PriceList
from app.schemas.price_list import CreatePrice, UpdatePrice


def create_price(
    session: Session,
    data: CreatePrice,
) -> PriceList:

    statement = select(PriceList).where(
        PriceList.garment == data.garment
    )

    existing_price = session.exec(statement).first()

    if existing_price:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Price already exists for this garment",
        )

    price = PriceList(
        garment=data.garment,
        unit_price=data.unit_price,
    )

    session.add(price)
    session.commit()
    session.refresh(price)

    return price


def get_prices(
    session: Session,
) -> list[PriceList]:

    statement = select(PriceList)

    return session.exec(statement).all()


def update_price(
    session: Session,
    price_id: int,
    data: UpdatePrice,
) -> PriceList:

    price = session.get(PriceList, price_id)

    if price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Price not found",
        )

    price.unit_price = data.unit_price

    session.add(price)
    session.commit()
    session.refresh(price)

    return price