from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=128)


class AccountCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=12, max_length=128)
    role: Literal["Resident", "Security"]
    resident_id: int | None = Field(default=None, gt=0)
    guard_id: int | None = Field(default=None, gt=0)

    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Username cannot be empty.")
        return value

    @model_validator(mode="after")
    def validate_role_link(self):
        if self.role == "Resident":
            if self.resident_id is None or self.guard_id is not None:
                raise ValueError(
                    "Resident accounts require resident_id only."
                )

        if self.role == "Security":
            if self.guard_id is None or self.resident_id is not None:
                raise ValueError(
                    "Security accounts require guard_id only."
                )

        return self
