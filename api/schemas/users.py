from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    user: str
    last_modified: datetime = Field(default_factory=datetime.now)