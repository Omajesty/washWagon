from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.models.user import Role, User
from app.schemas.price_list import (
    CreatePrice,
    PriceOut,
    UpdatePrice,
)
from app.services.dependencies import (
    get_current_user,
    require_role,
)
from app.services.price_list import (
    create_price,
    get_prices,
    update_price,
)
from app.utils.database import get_session


router = APIRouter(
    prefix="/prices",
    tags=["Prices"],
)


@router.post(
    "/",
    response_model=PriceOut,
    status_code=status.HTTP_201_CREATED,
)
def create_price_route(
    data: CreatePrice,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    return create_price(
        session=session,
        data=data,
    )


@router.get(
    "/",
    response_model=list[PriceOut],
)
def list_prices(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_prices(session)


@router.patch(
    "/{price_id}",
    response_model=PriceOut,
)
def update_price_route(
    price_id: int,
    data: UpdatePrice,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    return update_price(
        session=session,
        price_id=price_id,
        data=data,
    )