import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.models.user import Role, User
from app.schemas.user import UserOut
from app.utils.config import settings
from app.utils.database import get_session
from app.services.auth import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> UserOut:

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

    except jwt.InvalidTokenError:
        raise credentials_error

    user_id = payload.get("sub")

    if user_id is None:
        raise credentials_error

    user = get_user_by_id(
        session,
        int(user_id),
    )

    if user is None:
        raise credentials_error

    return user


def require_role(*allowed_roles: Role):

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return role_checker