from fastapi import APIRouter, Query, Depends
from typing import List

from app.database.database import database

from app.interfaces.schemas.fund_name_schema import FundList
from app.interfaces.schemas.transaction_schema import FundModel, TransactionUpdate, GetTransactions

from app.application.services.transaction_services import TransactionServices

fund_router = APIRouter(
    prefix="/api/v1/fund",
    tags=["fund"],
    responses={404: {"description": "Not found"}}
)


@fund_router.post('/link_fund/{account_id}')
async def link_fund(
        account_id: str,
        fund: FundList = Query(None),
        amount: float = Query(gt=0),
        db=Depends(database.get_database)
):
    new_transaction = TransactionUpdate(
        account_id=account_id,
        amount=None,
        fund_name=fund,
        fund_amount=amount
    )

    await TransactionServices(database=db).link_fund(new_transaction)
    return {"message": "Fund linked successfully"}


@fund_router.post('/unlink_fund/{account_id}')
async def unlink_fund(
        account_id: str,
        fund: FundList = Query(None),
        db=Depends(database.get_database)
):
    fund = FundModel(
        account_id=account_id,
        fund_name=fund
    )

    await TransactionServices(database=db).unlink_fund(fund)
    return {"message": "Fund unlinked successfully"}


@fund_router.get('/get_transactions/{account_id}')
async def get_funds(
        transactions_window:  GetTransactions = Query(None),
        db=Depends(database.get_database)
):
    return await TransactionServices(database=db).get_transactions(transactions_window)
