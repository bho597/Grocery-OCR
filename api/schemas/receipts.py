from datetime import date, time, datetime

from typing import Optional
from pydantic import BaseModel, field_validator, ValidationInfo, Field


class Receipt(BaseModel):
    blob_name: str
    MerchantName: str = None
    Subtotal: Optional[float] = None
    TotalTax: Optional[float] = None
    Total: float
    TransactionDate: Optional[date] = None
    TransactionTime: Optional[time] = None
    created_on: datetime = Field(default_factory=datetime.now)
    last_modified: datetime = Field(default_factory=datetime.now)
    textract_verified: bool = False
    payment_settled: bool = False
    paid_by: Optional[int] = None


    @field_validator("Total", "Subtotal", "TotalTax", mode="before")
    def validate_transaction_total(cls, v):
        return round(v, 2)

    @field_validator("Total", mode="after")
    def validate_total(cls, v: str, info: ValidationInfo):
        subtotal = info.data.get('Subtotal')
        total_tax = info.data.get('TotalTax')
        if subtotal and total_tax and v != round(subtotal + total_tax, 2):
            raise ValueError(f'Total, Subtotal, and TotalTax do not add up. Please verify the values before continuing.')
        return v


