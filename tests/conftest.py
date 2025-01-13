import os

from pytest import fixture

from tradestation import Session


# Run all tests with asyncio only
@fixture(scope="session")
def aiolib():
    return "asyncio"


@fixture(scope="session")
def credentials():
    username = os.getenv("TS_USERNAME")
    password = os.getenv("TS_PASSWORD")
    assert username is not None
    assert password is not None
    return username, password


@fixture(scope="session")
async def session(credentials, aiolib):
    session = Session(*credentials)
    yield session
    # session.destroy()
