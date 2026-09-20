from sqlmodel import SQLModel, Field

class Zone(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str