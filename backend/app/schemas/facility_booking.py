from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


BookingStatus = Literal[
    "Pending", "Approved", "Rejected", "Cancelled", "Completed"
]


class FacilityBookingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    facility_id: int = Field(gt=0)
    resident_id: int | None = Field(default=None, gt=0)
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time.")
        return self


class FacilityBookingStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    booking_status: BookingStatus


class FacilityBookingResponse(BaseModel):
    booking_id: int
    facility_id: int
    resident_id: int
    start_time: datetime
    end_time: datetime
    booking_status: str
    created_at: datetime
