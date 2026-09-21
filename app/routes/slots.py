from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.models.user import Role, User
from app.schemas.slots import (
    CreateSlot,
    UpdateSlot,
    SlotOut,
)
from app.services.dependencies import (
    get_current_user,
    require_role,
)
from app.services.slots import (
    create_slot,
    get_slots,
    get_slot,
    update_slot,
)
from app.utils.database import get_session


router = APIRouter(
    prefix="/slots",
    tags=["Slots"],
)


@router.post(
    "/",
    response_model=SlotOut,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: CreateSlot,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    return create_slot(
        session=session,
        data=data,
    )


@router.get(
    "/",
    response_model=list[SlotOut],
)
def list_all(
    zone_id: int | None = Query(default=None, gt=0),
    slot_date: date | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_slots(
        session=session,
        zone_id=zone_id,
        slot_date=slot_date,
    )


@router.get(
    "/{slot_id}",
    response_model=SlotOut,
)
def read(
    slot_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_slot(
        session=session,
        slot_id=slot_id,
    )


@router.patch(
    "/{slot_id}",
    response_model=SlotOut,
)
def update(
    slot_id: int,
    data: UpdateSlot,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    return update_slot(
        session=session,
        slot_id=slot_id,
        data=data,
    )
    