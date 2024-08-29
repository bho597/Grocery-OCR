from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator, Field


class LineItem(BaseModel):
    item_description: Optional[str]
    item_total_price: Optional[float]
    line_item_number: Optional[int] = None
    receipt_id: int
    is_taxed: bool = False
    bought_by: Optional[int] = None
    last_modified: datetime = Field(default_factory=datetime.now)


    @field_validator("item_total_price", mode="before")
    def validate_transaction_total(cls, v):
        if v is None:
            return v
        return round(v, 2)


class SplitRequest(BaseModel):
    quantity: List[float] = Field(min_length=1)

    @field_validator("quantity", mode="before")
    def validate_transaction_total(cls, v):
        if 1 - sum(v) > .001:
            raise ValueError('Ratios do not add up to 1')
        return v