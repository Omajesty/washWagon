from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.utils.database import get_session
from app.schemas.user import (
    TokenResponse,
    UserOut,
    UserRegister,
)
from app.services.user import (
    confirm_user,
    register_customer,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserRegister,
    session: Session = Depends(get_session),
):
    return register_customer(
        session,
        data,
    )



@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):

    token = confirm_user(
        session=session,
        email=form.username,
        password=form.password,
    )

    return TokenResponse(
        access_token=token,
    )
