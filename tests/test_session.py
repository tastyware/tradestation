from tradestation.session import Session


def test_session():
    session = Session()
    assert session is not None

