from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Category = Literal[
    "Plumbing", "Electrical", "Cleaning", "Lift",
    "Parking", "Security", "Common Area", "Other"
]
Priority = Literal["Low", "Medium", "High", "Urgent"]
ComplaintStatus = Literal[
    "Open", "Assigned", "In Progress", "Resolved", "Closed"
]


class ComplaintCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resident_id: int = Field(gt=0)
    vendor_id: int | None = Field(default=None, gt=0)
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    category: Category
    priority: Priority = "Medium"

    @field_validator("title", "description")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class ComplaintUpdate(ComplaintCreate):
    complaint_status: ComplaintStatus = "Open"


class ComplaintResponse(BaseModel):
    complaint_id: int
    resident_id: int
    vendor_id: int | None
    title: str
    description: str
    category: str
    priority: str
    complaint_status: str
    created_at: datetime
    resolved_at: datetime | None
