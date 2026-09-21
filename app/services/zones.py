from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.zones import Zone
from app.schemas.zones import CreateZone, UpdateZone


def create_zone(
    session: Session,
    data: CreateZone,
) -> Zone:

    existing_zone = session.exec(
        select(Zone).where(
            Zone.name == data.name
        )
    ).first()

    if existing_zone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Zone already exists",
        )

    zone = Zone(
        name=data.name,
    )

    session.add(zone)
    session.commit()
    session.refresh(zone)

    return zone


def get_zones(
    session: Session,
) -> list[Zone]:

    statement = select(Zone).order_by(Zone.id)

    return list(
        session.exec(statement).all()
    )


def get_zone(
    session: Session,
    zone_id: int,
) -> Zone:

    zone = session.get(
        Zone,
        zone_id,
    )

    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found",
        )

    return zone


def update_zone(
    session: Session,
    zone_id: int,
    data: UpdateZone,
) -> Zone:

    zone = session.get(
        Zone,
        zone_id,
    )

    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found",
        )

    existing_zone = session.exec(
        select(Zone).where(
            Zone.name == data.name,
            Zone.id != zone_id,
        )
    ).first()

    if existing_zone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Zone already exists",
        )

    zone.name = data.name

    session.add(zone)
    session.commit()
    session.refresh(zone)

    return zone