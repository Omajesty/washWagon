from pydantic import BaseModel, Field


class CreateZone(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    
class UpdateZone(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=25,
    )
    

class ZoneOut(BaseModel):
    id: int
    name: str