import uuid

from pydantic import BaseModel, Field
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    transaction_type: str
    fund_name: str = None
