from app.adapters.account_repository import AccountRepository


class AccountServices:
    def __init__(self, database):
        self.db = database
        self.account_repository = AccountRepository(db=self.db)

    async def create_account(self, request):
        return await self.account_repository.create_account(request)

