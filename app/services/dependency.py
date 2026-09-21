from sqlmodel import Session, select

from app.models.user import User


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


def create_user(
    session: Session,
    user: User,
) -> User:

    session.add(user)
    session.flush()
    return user
