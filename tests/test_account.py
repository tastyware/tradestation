from pytest import fixture

from tradestation import Account, Session


@fixture(scope="module")
def accounts(session: Session) -> list[Account]:
    return Account.get_accounts(session)


def test_get_accounts(accounts: list[Account]):
    assert accounts != []


async def test_get_accounts_async(session: Session):
    accounts = await Account.a_get_accounts(session)
    assert accounts != []


def test_get_balances(session: Session, accounts: list[Account]):
    balances = Account.get_balances(session, accounts)
    assert balances.balances != []


async def test_get_balances_async(session: Session, accounts: list[Account]):
    balances = await Account.a_get_balances(session, accounts)
    assert balances.balances != []
