from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApartmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    building_name: str = Field(min_length=1, max_length=100)
    flat_number: str = Field(min_length=1, max_length=20)
    floor_number: int | None = Field(default=None, ge=0)

    @field_validator("building_name", "flat_number")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value


class ApartmentUpdate(ApartmentCreate):
    pass


class ApartmentResponse(BaseModel):
    apartment_id: int
    building_name: str
    flat_number: str
    floor_number: int | None
