from enum import Enum
from fastapi import Query
from pydantic import BaseModel, model_validator


class AccountBase(BaseModel):
    owner: str


class AccountCreateRequest(AccountBase):
    notification: str | None = "email"
    balance: int | None = None
    active: bool | None = None
    active_funds: dict = dict()

    @model_validator(mode='after')
    def balance_setter(self):
        self.balance = 500000
        self.active = True
        return self

    @model_validator(mode='after')
    def balance_validator(self):
        if self.balance <= 0:
            raise ValueError("Balance must be greater than 0")
        return self

    @model_validator(mode='after')
    def notification_validator(self):
        if self.notification not in ("email", "sms"):
            raise ValueError("Not a valid notification device")
        return self


class AccountResponse(BaseModel):
    account_id: str
    balance: int
    active_funds: dict | None
    notification: str
