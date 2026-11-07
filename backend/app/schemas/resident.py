import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResidentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    phone: str | None = Field(default=None, max_length=15)
    apartment_id: int = Field(gt=0)

    @field_validator("full_name", "email")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Enter a valid email address.")
        return value.lower()

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class ResidentUpdate(ResidentCreate):
    pass


class ResidentResponse(BaseModel):
    resident_id: int
    full_name: str
    email: str
    phone: str | None
    apartment_id: int


class ResidentDetailResponse(ResidentResponse):
    building_name: str
    flat_number: str
