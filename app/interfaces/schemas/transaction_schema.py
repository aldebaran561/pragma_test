from pydantic import BaseModel, model_validator
from datetime import datetime, timedelta

from app.utils.date_converter import GMT


class AccountBase(BaseModel):
    account_id: str


class FundModel(AccountBase):
    fund_name: str


class TransactionUpdate(FundModel):
    amount: float | None
    fund_amount: float


class GetTransactions(AccountBase):
    start_date: datetime = (datetime.now(GMT) - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    end_date: datetime = datetime.now(GMT).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    @model_validator(mode='after')
    def date_validator(self):
        if self.start_date > self.end_date:
            raise ValueError("Start date greater than End date")
        return self


class AllTransactions(BaseModel):
    timestamp: datetime
    transaction_type: str
    fund_name: str
    amount: float
