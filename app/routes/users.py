from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from app.models.user import Role, User
from app.schemas.user import CourierCreate, UserOut
from app.services.dependencies import (
    get_current_user,
    require_role,
)
from app.services.user import create_courier
from app.utils.database import get_session


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserOut,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/",
    response_model=list[UserOut],
)
def list_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    statement = select(User)

    return session.exec(statement).all()


@router.post(
    "/couriers",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_courier_account(
    data: CourierCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(
        require_role(Role.OPS_MANAGER)
    ),
):
    return create_courier(
        session=session,
        data=data,
    )