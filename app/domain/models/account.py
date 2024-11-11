from pydantic import BaseModel, Field
from typing import Optional


class Account(BaseModel):
    account_id: str
    balance: float = Field(default=500000)
    owner: str
    active: bool
