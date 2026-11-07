from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PaymentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bill_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    payment_method: Literal["Cash", "UPI", "Card", "Bank Transfer"]
    transaction_reference: str | None = Field(default=None, max_length=100)
    payment_status: Literal["Pending", "Completed", "Failed"] = "Completed"

    @field_validator("transaction_reference")
    @classmethod
    def normalize_reference(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class PaymentResponse(BaseModel):
    payment_id: int
    bill_id: int
    amount: Decimal
    payment_date: datetime
    payment_method: str
    transaction_reference: str | None
    payment_status: str
