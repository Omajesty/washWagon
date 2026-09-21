

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.user import Role, User
from app.schemas.user import  UserOut, UserRegister
from app.services.dependency import create_user, get_user_by_email
from app.utils.security import hash_password


def register_customer(
        session:Session,
        data:UserRegister
) -> UserOut:

    existing_user = get_user_by_email(
        session, data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=Role.CUSTOMER,
        zone_id=data.zone,
    )

    create_user(session,user)

    session.commit()
    session.refresh(user)

    return user
