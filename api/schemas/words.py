from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field


class Word(BaseModel):
    word: str
    word_index: int
    line_index: Optional[int]
    confidence: Optional[float]
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    receipt_id: int
    last_modified: datetime = Field(default_factory=datetime.now)