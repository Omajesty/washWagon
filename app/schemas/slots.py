from datetime import date, time

from pydantic import BaseModel, Field, model_validator


class CreateSlot(BaseModel):
    zone_id: int = Field(gt=0)
    capacity: int = Field(gt=0)
    date: date
    start_at: time
    stop_at: time

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_at >= self.stop_at:
            raise ValueError("stop_at must be after start_at")

        return self


class UpdateSlot(BaseModel):
    capacity: int = Field(gt=0)
    date: date
    start_at: time
    stop_at: time

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_at >= self.stop_at:
            raise ValueError("stop_at must be after start_at")

        return self


class SlotOut(BaseModel):
    id: int
    zone_id: int
    capacity: int
    booked_count: int
    date: date
    start_at: time
    stop_at: time