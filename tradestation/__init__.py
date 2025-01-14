import logging

API_URL_V3 = "https://api.tradestation.com/v3"
API_URL_V2 = "https://api.tradestation.com/v2"
API_URL_SIM = "https://sim-api.tradestation.com/v3"
OAUTH_SCOPES = [
    # Requests access to lookup or stream Market Data.
    "MarketData",
    # Requests access to view Brokerage Accounts belonging to the current user.
    "ReadAccount",
    # Requests access to execute orders on behalf of the current user's account(s).
    "Trade",
    # Request access to execute options related endpoints.
    "OptionSpreads",
    # Request access to execute market depth related endpoints.
    "Matrix",
    # Returns the sub claim, which uniquely identifies the user. In an ID Token, iss, aud, exp, iat, and at_hash claims will also be present.
    "openid",
    # Allows for use of Refresh Tokens.
    "offline_access",
    # Returns claims in the ID Token that represent basic profile information, including name, family_name, given_name, middle_name, nickname, picture, and updated_at.
    "profile",
    # Returns the email claim in the ID Token, which contains the user's email address, and email_verified, which is a boolean indicating whether the email address was verified by the user.
    "email",
]
OAUTH_URL = "https://signin.tradestation.com"
VERSION = "0.2"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ruff: noqa: E402

from .account import Account
from .session import AutoRefreshSession, Session

__all__ = ["Account", "AutoRefreshSession", "Session"]
