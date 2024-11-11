from fastapi import APIRouter, Depends, Query

from app.database.database import database

from app.application.services.acount_services import AccountServices

from app.interfaces.schemas.account_schema import AccountCreateRequest


account_router = APIRouter(
    prefix="/api/v1/account",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)


@account_router.post("/create")
async def create_account(
        new_account: AccountCreateRequest,
        db=Depends(database.get_database)
):
    await AccountServices(database=db).create_account(new_account)
    return {"message": "Account created successfully"}
