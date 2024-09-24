import logging

from .session import Session

API_URL_V3 = 'https://api.tradestation.com/v3'
API_URL_V2 = 'https://api.tradestation.com/v2'
API_URL_SIM = 'https://sim-api.tradestation.com/v3'
VERSION = '0.1'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

__all__ = ['Session']

