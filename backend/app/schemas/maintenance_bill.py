from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MaintenanceBillCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    apartment_id: int = Field(gt=0)
    billing_month: date
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    due_date: date


class MaintenanceBillUpdate(MaintenanceBillCreate):
    pass


class MaintenanceBillResponse(BaseModel):
    bill_id: int
    apartment_id: int
    billing_month: date
    amount: Decimal
    due_date: date
    bill_status: str
    created_at: datetime
    paid_amount: Decimal
    outstanding_amount: Decimal
