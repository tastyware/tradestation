import asyncio

import pytest

from tradestation.session import AutoRefreshSession, Session
from tradestation.utils import TradestationError


def test_invalid_response():
    with pytest.raises(TradestationError):
        _ = Session("api_key", "secret_key", "refresh_token")


def test_refresh(session: Session):
    session.refresh()


async def test_refresh_async(session: Session):
    await session.a_refresh()


def test_user_info(session: Session):
    assert "email" in session.user_info


def test_serialize_deserialize(session: Session):
    data = session.serialize()
    obj = Session.deserialize(data)
    assert set(obj.__dict__.keys()) == set(session.__dict__.keys())


async def test_auto_refresh_constructor(session: Session):
    ars = await AutoRefreshSession(
        session.api_key,
        session.secret_key,
        session.refresh_token,
        session.access_token,
        token_lifetime=0,
        is_test=True,
    )
    await asyncio.sleep(3)
    assert ars.token_lifetime != 0
    await ars.close()


async def test_auto_refresh_context_manager(session: Session):
    async with AutoRefreshSession(
        session.api_key,
        session.secret_key,
        session.refresh_token,
        session.access_token,
        token_lifetime=0,
        is_test=True,
    ) as ars:
        await asyncio.sleep(3)
        assert ars.token_lifetime != 0
