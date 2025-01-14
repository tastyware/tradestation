import os
from typing import AsyncGenerator

from pytest import fixture

from tradestation import Session


# Run all tests with asyncio only
@fixture(scope="session")
def aiolib() -> str:
    return "asyncio"


@fixture(scope="session")
def credentials() -> tuple[str, str, str]:
    api_key = os.getenv("TS_API_KEY")
    secret_key = os.getenv("TS_SECRET_KEY")
    refresh_token = os.getenv("TS_REFRESH")
    assert api_key is not None
    assert secret_key is not None
    assert refresh_token is not None
    return api_key, secret_key, refresh_token


@fixture(scope="session")
async def session(
    credentials: tuple[str, str, str], aiolib: str
) -> AsyncGenerator[Session, None]:
    session = Session(*credentials, is_test=True)
    yield session
