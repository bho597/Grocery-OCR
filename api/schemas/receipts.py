from datetime import date, time, datetime

from typing import Optional
from pydantic import BaseModel, field_validator, ValidationInfo, Field


class Receipt(BaseModel):
    blob_name: str
    merchant_name: str = None
    subtotal: Optional[float] = None
    total_tax: Optional[float] = None
    total: float
    transaction_date: Optional[date] = None
    transaction_time: Optional[time] = None
    created_on: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    textract_verified: bool = False
    payment_settled: bool = False
    paid_by: Optional[int] = None


    @field_validator("total", "subtotal", "total_tax", mode="before")
    def validate_transaction_total(cls, v):
        return round(v, 2)

    @field_validator("total", mode="after")
    def validate_total(cls, v: str, info: ValidationInfo):
        subtotal = info.data.get('subtotal')
        total_tax = info.data.get('total_tax')
        if subtotal and total_tax and v != round(subtotal + total_tax, 2):
            raise ValueError(f'total, subtotal, and total_tax do not add up. Please verify the values before continuing.')
        return v


