from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.user import User
from app.models.zones import Zone
from app.schemas.user import TokenResponse, UserLogin
from app.utils.security import create_access_token, verify_password


def get_user_by_email(
    session: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return session.exec(statement).first()


def get_user_by_id(
    session: Session,
    user_id: int,
) -> User | None:
    return session.get(User, user_id)


def get_zone_by_name(
    session: Session,
    name: str,
) -> Zone | None:
    statement = select(Zone).where(Zone.name == name)

    return session.exec(statement).first()


def create_user(
    session: Session,
    user: User,
) -> User:
    session.add(user)
    session.flush()

    return user


def login_user(
    session: Session,
    data: UserLogin,
) -> TokenResponse:
    user = get_user_by_email(session, data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    password_is_valid = verify_password(
        data.password,
        user.hashed_password,
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
