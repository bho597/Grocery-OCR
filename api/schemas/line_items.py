from pydantic import BaseModel, field_validator


class LineItem(BaseModel):
    item_description: str
    item_total_price: float
    receipt_id: int
    line_id: int


    @field_validator("item_total_price", mode="before")
    def validate_transaction_total(cls, v):
        return round(v, 2)
