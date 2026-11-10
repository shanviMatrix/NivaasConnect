from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


EventStatus = Literal["Planned", "Ongoing", "Completed", "Cancelled"]


class SocietyEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_title: str = Field(min_length=1, max_length=150)
    description: str | None = None
    venue: str = Field(min_length=1, max_length=150)
    start_time: datetime
    end_time: datetime
    created_by: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time.")
        return self


class SocietyEventUpdate(SocietyEventCreate):
    event_status: EventStatus = "Planned"


class SocietyEventResponse(BaseModel):
    event_id: int
    event_title: str
    description: str | None
    venue: str
    start_time: datetime
    end_time: datetime
    created_by: int
    event_status: str
    created_at: datetime
