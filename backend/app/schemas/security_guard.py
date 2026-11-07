from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SecurityGuardCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=1, max_length=15)
    shift_name: Literal["Morning", "Evening", "Night", "Rotational"]
    is_active: bool = True

    @field_validator("full_name", "phone")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class SecurityGuardUpdate(SecurityGuardCreate):
    pass


class SecurityGuardResponse(BaseModel):
    guard_id: int
    full_name: str
    phone: str
    shift_name: str
    is_active: bool
    created_at: datetime
