import pytest
import signal

from tradestation.oauth import (
    Credentials,
    get_access_url,
    convert_auth_code,
    login,
    response_page,
)


def test_get_access_url():
    credentials = Credentials(key="test")
    url = get_access_url(credentials)
    assert "test" in url


def test_convert_auth_code():
    with pytest.raises(Exception):
        convert_auth_code(Credentials(), "bogus")


def test_response_page():
    page = response_page("refresh", "access", {"key": "value"})
    assert isinstance(page, bytes)


def handler(signum, frame):
    raise TimeoutError


def test_login():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(3)
    with pytest.raises(TimeoutError):
        login()
