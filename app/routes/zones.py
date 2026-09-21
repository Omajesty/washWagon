from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.models.user import Role, User
from app.schemas.zones import (
    CreateZone,
    UpdateZone,
    ZoneOut,
)
from app.services.dependencies import require_role, get_current_user
from app.services.zones import (
    create_zone,
    get_zones,
    get_zone,
    update_zone,
)
from app.utils.database import get_session


router = APIRouter(
    prefix="/zones",
    tags=["Zones"],
)


@router.post(
    "/",
    response_model=ZoneOut,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: CreateZone,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    return create_zone(
        session=session,
        data=data,
    )


@router.get(
    "/",
    response_model=list[ZoneOut],
)
def list_zones(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_zones(
        session=session,
    )


@router.get(
    "/{zone_id}",
    response_model=ZoneOut,
)
def read_zone(
    zone_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_zone(
        session=session,
        zone_id=zone_id,
    )


@router.patch(
    "/{zone_id}",
    response_model=ZoneOut,
)
def update(
    zone_id: int,
    data: UpdateZone,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    return update_zone(
        session=session,
        zone_id=zone_id,
        data=data,
    )
    