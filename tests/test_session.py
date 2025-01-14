import os

from tradestation.session import Session


def test_session():
    api_key = os.getenv("TS_API_KEY")
    secret_key = os.getenv("TS_SECRET_KEY")
    refresh_token = os.getenv("TS_REFRESH")
    assert api_key is not None
    assert secret_key is not None
    assert refresh_token is not None
    session = Session(api_key, secret_key, refresh_token)
    assert session.user_info != {}
