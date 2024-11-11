from app.domain.models.transaction import Transaction

from app.interfaces.schemas.transaction_schema import AllTransactions


class TransactionRepository:
    def __init__(self, db):
        self.transactions_collection = db.transactions

    async def create_transaction(self, transaction: Transaction):
        await self.transactions_collection.insert_one(transaction.model_dump())

    async def get_transactions(self, transactions_window):
        query = {
            "account_id": transactions_window.account_id,
            "timestamp": {
                "$gte": transactions_window.start_date,
                "$lte": transactions_window.end_date
            }
        }

        transactions = await self.transactions_collection.find(query).sort("timestamp", -1).to_list(None)
        return [AllTransactions(**transaction) for transaction in transactions]
