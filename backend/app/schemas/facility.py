from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class FacilityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    facility_name: str = Field(min_length=1, max_length=100)
    location_description: str | None = Field(default=None, max_length=150)
    capacity: int | None = Field(default=None, gt=0)
    booking_fee: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
    is_active: bool = True


class FacilityUpdate(FacilityCreate):
    pass


class FacilityResponse(FacilityCreate):
    facility_id: int
