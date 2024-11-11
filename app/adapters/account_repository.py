from bson import ObjectId

from app.domain.models.account import Account

from app.interfaces.schemas.account_schema import AccountResponse


class AccountRepository:
    def __init__(self, db):
        self.accounts_collection = db.accounts

    async def create_account(self, account):
        await self.accounts_collection.insert_one(account.model_dump())

    async def get_account(self, account_id):
        account_data = await self.accounts_collection.find_one({"_id": ObjectId(account_id)})
        if account_data:
            return AccountResponse(
                account_id=str(account_data.get('_id')),
                balance=account_data.get('balance'),
                active_funds=account_data.get('active_funds'),
                notification=account_data.get('notification')
            )
        return

    async def update_balance(self, account_data):
        await self.accounts_collection.update_one(
            {"_id": ObjectId(account_data.account_id), "active_funds": {"$exists": False}},
            {"$set": {"active_funds": {}}}
        )

        await self.accounts_collection.update_one(
            {"_id": ObjectId(account_data.account_id)},
            {
                "$set": {
                    "balance": account_data.amount,
                    f"active_funds.{account_data.fund_name}": account_data.fund_amount
                }
            }
        )

    async def remove_fund(self, fund_name, account_data):
        await self.accounts_collection.update_one(
            {"_id": ObjectId(account_data.account_id)},
            {
                "$inc": {
                    "balance": account_data.active_funds.get(fund_name)
                },
                "$unset": {
                    f"active_funds.{fund_name}": ""
                }
            }
        )
