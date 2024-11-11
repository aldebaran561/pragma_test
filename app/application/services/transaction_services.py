from app.adapters.account_repository import AccountRepository
from app.adapters.transaction_repository import TransactionRepository
from app.domain.models.transaction import Transaction
from app.exceptions.exception_handler import InvalidRequest


class TransactionServices:
    def __init__(self, database):
        self.db = database
        self.account_repository = AccountRepository(self.db)
        self.transaction_repository = TransactionRepository(self.db)

    async def link_fund(self, transaction):

        minimum_needed = self.__get_minimum_value_on_fund(transaction.fund_name)
        if transaction.fund_amount < minimum_needed:
            raise InvalidRequest(detail=f"Amount must be greater than {minimum_needed}")

        account = await self.__get_account(transaction.account_id)

        transaction.amount = account.balance - transaction.fund_amount

        if transaction.amount < 0:
            raise InvalidRequest(detail='Insufficient balance')

        await self.account_repository.update_balance(transaction)

        transaction = Transaction(
            account_id=transaction.account_id,
            amount=transaction.amount,
            transaction_type="fund_linking",
            fund_name=transaction.fund_name
        )
        await self.transaction_repository.create_transaction(transaction)

        self.__send_notification(account.notification)

    async def unlink_fund(self, active_fund):
        account = await self.__get_account(active_fund.account_id)

        if active_fund.fund_name not in account.active_funds:
            raise InvalidRequest(detail='Fund not found')

        await self.account_repository.remove_fund(active_fund.fund_name, account)

        transaction = Transaction(
            account_id=account.account_id,
            amount=account.active_funds.get(active_fund.fund_name),
            transaction_type="fund_unlinking",
            fund_name=active_fund.fund_name
        )
        await self.transaction_repository.create_transaction(transaction)

        self.__send_notification(account.notification)

    async def get_transactions(self, transactions_window):
        await self.__get_account(transactions_window.account_id)

        all_transactions = await self.transaction_repository.get_transactions(transactions_window)

        return all_transactions

    async def __get_account(self, account_id):
        account = await self.account_repository.get_account(account_id)
        if not account:
            raise InvalidRequest(detail='Account not found')
        return account

    def __send_notification(self, notification_device):
        pass #TODO define how to send (Lambda, Event Bridge & SNS)

    @staticmethod
    def __get_minimum_value_on_fund(fund_name):
        funds = {
            "FPV_BTG_PACTUAL_RECAUDADORA": 75000,
            "FPV_BTG_PACTUAL_ECOPETROL": 125000,
            "DEUDAPRIVADA": 50000,
            "FDO_ACCIONES": 250000,
            "FPV_BTG_PACTUAL_DINAMICA": 100000
        }

        return funds.get(fund_name)
