

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.user import Role, User
from app.schemas.user import UserRegister
from app.services.auth import (
    create_user,
    get_user_by_email,
    get_zone_by_name,
)
from app.utils.security import create_access_token, hash_password, verify_password


def register_customer(
    session: Session,
    data: UserRegister,
) -> User:

    existing_user = get_user_by_email(
        session, data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    zone = get_zone_by_name(session, data.zone)

    if zone is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found",
        )

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=Role.CUSTOMER,
        zone_id=zone.id,
    )

    create_user(session, user)

    session.commit()
    session.refresh(user)

    return user


def confirm_user(
        session: Session,
        email:str,
        password: str,
) -> str:

    user = get_user_by_email(session, email)

    if user is None or not verify_password(
        password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    token = create_access_token(
        user_id=user.id,
        role=user.role.value
    )

    return token