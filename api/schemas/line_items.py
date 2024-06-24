from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, Field


class LineItem(BaseModel):
    item_description: Optional[str]
    item_total_price: Optional[float]
    line_item_number: Optional[int]
    receipt_id: int
    is_taxed: bool = False
    bought_by: Optional[int] = None
    last_modified: datetime = Field(default_factory=datetime.now)


    @field_validator("item_total_price", mode="before")
    def validate_transaction_total(cls, v):
        if v is None:
            return v
        return round(v, 2)
