from pydantic import Field

from tradestation.utils import TradestationModel


class AccountDetail(TradestationModel):
    day_trading_qualified: bool
    enrolled_in_reg_t_program: bool
    is_stock_locate_eligible: bool
    option_approval_level: int
    pattern_day_trader: bool
    requires_buying_power_warning: bool


class Account(TradestationModel):
    account_detail: AccountDetail | None = None
    account_id: str = Field(alias="AccountID")
    account_type: str
    alias: str | None = None
    alt_id: str | None = Field(default=None, alias="AltID")
    currency: str
    status: str
