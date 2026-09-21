from datetime import date

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.slots import Slot
from app.models.zones import Zone
from app.schemas.slots import CreateSlot, UpdateSlot


def create_slot(
    session: Session,
    data: CreateSlot,
) -> Slot:

    zone = session.get(Zone, data.zone_id)

    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found",
        )

    existing_slot = session.exec(
        select(Slot).where(
            Slot.zone_id == data.zone_id,
            Slot.date == data.date,
            Slot.start_at == data.start_at,
            Slot.stop_at == data.stop_at,
        )
    ).first()

    if existing_slot:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot already exists for this zone and time",
        )

    slot = Slot(
        zone_id=data.zone_id,
        capacity=data.capacity,
        date=data.date,
        start_at=data.start_at,
        stop_at=data.stop_at,
    )

    session.add(slot)
    session.commit()
    session.refresh(slot)

    return slot


def get_slots(
    session: Session,
    zone_id: int | None = None,
    slot_date: date | None = None,
) -> list[Slot]:

    statement = select(Slot).order_by(
        Slot.date,
        Slot.start_at,
        Slot.id,
    )

    if zone_id is not None:
        statement = statement.where(
            Slot.zone_id == zone_id
        )

    if slot_date is not None:
        statement = statement.where(
            Slot.date == slot_date
        )

    return list(session.exec(statement).all())


def get_slot(
    session: Session,
    slot_id: int,
) -> Slot:

    slot = session.get(Slot, slot_id)

    if slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slot not found",
        )

    return slot


def update_slot(
    session: Session,
    slot_id: int,
    data: UpdateSlot,
) -> Slot:

    slot = session.get(Slot, slot_id)

    if slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slot not found",
        )

    if data.capacity < slot.booked_count:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Capacity cannot be less than "
                "the current booked count"
            ),
        )

    existing_slot = session.exec(
        select(Slot).where(
            Slot.zone_id == slot.zone_id,
            Slot.date == data.date,
            Slot.start_at == data.start_at,
            Slot.stop_at == data.stop_at,
            Slot.id != slot_id,
        )
    ).first()

    if existing_slot:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slot already exists for this zone and time",
        )

    slot.capacity = data.capacity
    slot.date = data.date
    slot.start_at = data.start_at
    slot.stop_at = data.stop_at

    session.add(slot)
    session.commit()
    session.refresh(slot)

    return slot