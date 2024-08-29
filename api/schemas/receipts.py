from datetime import date, time, datetime

from typing import Optional, List
from pydantic import BaseModel, field_validator, Field


class Receipt(BaseModel):
    blob_name: str
    merchant_name: Optional[str] = None
    subtotal: Optional[float] = None
    total_tax: Optional[float] = 0
    total_tax_percent: Optional[float] = None
    discount: float = 0
    total: float
    transaction_date: Optional[date] = None
    transaction_time: Optional[time] = None
    created_on: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    textract_verified: bool = False
    payment_settled: bool = False
    paid_by: Optional[int] = None
    bought_by: Optional[List[int]] = None


    @field_validator("total", "subtotal", "total_tax", mode="before")
    def validate_transaction_total(cls, v):
        if v is None:
            return v
        return round(v, 2)


