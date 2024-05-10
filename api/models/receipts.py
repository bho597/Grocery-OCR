from datetime import date, datetime

from typing import Optional
from pydantic import BaseModel, AnyHttpUrl, validator


class Receipt(BaseModel):
    filename: str
    merchant_name: str
    # receipt_date: date
    receipt_date: str
    image_url: AnyHttpUrl
    # transaction_date : date
    transaction_date : str
    transaction_time : Optional[str]
    # modified_date : date
    modified_date : str
    textracted: bool = False
    verified: bool = False

    # @validator("receipt_date", "transaction_date", "modified_date", pre=True)
    # def string_to_date(cls, v: object) -> object:
    #     if isinstance(v, str):
    #         return datetime.strptime(v, '%Y-%m-%d').date()
    #     return v

