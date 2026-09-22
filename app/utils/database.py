from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.utils.config import settings


if not settings.DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Add it to your .env file before starting the API."
    )

engine = create_engine(settings.DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
