from sqlmodel import SQLModel, Field

class Zones(SQLModel, table=True):
    id: int
    name: str