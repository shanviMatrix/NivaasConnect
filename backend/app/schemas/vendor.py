import re

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class VendorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vendor_name: str = Field(min_length=1, max_length=120)
    service_category: str = Field(min_length=1, max_length=80)
    phone: str | None = Field(default=None, max_length=15)
    email: str | None = Field(default=None, max_length=150)
    is_active: bool = True

    @field_validator("vendor_name", "service_category")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

    @field_validator("phone", "email")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Enter a valid email address.")
        return value.lower()


class VendorUpdate(VendorCreate):
    pass


class VendorResponse(BaseModel):
    vendor_id: int
    vendor_name: str
    service_category: str
    phone: str | None
    email: str | None
    is_active: bool
    created_at: datetime
