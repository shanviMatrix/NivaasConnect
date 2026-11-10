from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


ApprovalStatus = Literal["Pending", "Approved", "Denied"]


class VisitorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resident_id: int = Field(gt=0)
    guard_id: int | None = Field(default=None, gt=0)
    visitor_name: str = Field(min_length=1, max_length=100)
    visitor_phone: str | None = Field(default=None, max_length=15)
    purpose: str = Field(min_length=1, max_length=200)

    @field_validator("visitor_name", "purpose")
    @classmethod
    def clean_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

    @field_validator("visitor_phone")
    @classmethod
    def normalize_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class VisitorApprovalUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approval_status: ApprovalStatus


class VisitorResponse(BaseModel):
    visitor_id: int
    resident_id: int
    guard_id: int
    visitor_name: str
    visitor_phone: str | None
    purpose: str
    entry_time: datetime
    exit_time: datetime | None
    approval_status: str
