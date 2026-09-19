from pydantic import EmailStr
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int
    name: str
    email: EmailStr
    hashed_pasword: str
    role: str
    zone_id: int
    