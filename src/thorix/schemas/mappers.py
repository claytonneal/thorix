from thorix.types.account import Account

from .account import AccountSchema


def map_account(schema: AccountSchema) -> Account:
    """
    Maps an AccountSchema to an Account
    """
    return Account(
        balance=schema.balance,
        energy=schema.energy,
        has_code=schema.has_code,
    )
