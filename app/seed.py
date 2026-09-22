from sqlmodel import Session, select

from app.models.user import Role, User
from app.utils.config import settings
from app.utils.database import engine
from app.utils.security import hash_password


def create_ops_manager() -> None:
    with Session(engine) as session:
        statement = select(User).where(
            User.email == settings.OPS_MANAGER_EMAIL
        )

        existing_user = session.exec(statement).first()

        if existing_user:
            print(
                f"User with email {settings.OPS_MANAGER_EMAIL} "
                "already exists."
            )
            return

        ops_manager = User(
            name=settings.OPS_MANAGER_NAME,
            email=settings.OPS_MANAGER_EMAIL,
            hashed_password=hash_password(
                settings.OPS_MANAGER_PASSWORD
            ),
            role=Role.OPS_MANAGER,
        )

        session.add(ops_manager)
        session.commit()
        session.refresh(ops_manager)

        print(
            f"Ops Manager created successfully. "
            f"User ID: {ops_manager.id}"
        )


if __name__ == "__main__":
    create_ops_manager()