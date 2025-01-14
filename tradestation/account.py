from decimal import Decimal
from pydantic import Field
from typing_extensions import Self

from tradestation.session import Session
from tradestation.utils import TradestationModel


class AccountDetail(TradestationModel):
    day_trading_qualified: bool
    enrolled_in_reg_t_program: bool
    is_stock_locate_eligible: bool
    option_approval_level: int
    pattern_day_trader: bool
    requires_buying_power_warning: bool


class AccountBalanceDetail(TradestationModel):
    cost_of_positions: Decimal | None = None
    day_trade_excess: Decimal | None = None
    day_trade_margin: Decimal | None = None
    day_trade_open_order_margin: Decimal | None = None
    day_trades: int | None = None
    initial_margin: Decimal | None = None
    maintenance_margin: Decimal | None = None
    maintenance_rate: Decimal | None = None
    margin_requirement: Decimal | None = None
    open_order_margin: Decimal | None = None
    option_buying_power: Decimal | None = None
    options_market_value: Decimal | None = None
    overnight_buying_power: Decimal | None = None
    required_margin: Decimal | None = None
    realized_profit_loss: Decimal
    security_on_deposit: Decimal | None = None
    today_real_time_trade_equity: Decimal | None = None
    trade_equity: Decimal | None = None
    unrealized_profit_loss: Decimal
    unsettled_funds: Decimal | None = None


class AccountCurrencyDetail(TradestationModel):
    currency: str
    commission: Decimal
    cash_balance: Decimal
    realized_profit_loss: Decimal
    unrealized_profit_loss: Decimal
    initial_margin: Decimal
    maintenance_margin: Decimal
    account_conversion_rate: Decimal
    account_margin_requirement: Decimal | None = None


class AccountBalance(TradestationModel):
    account_id: str = Field(alias="AccountID")
    account_type: str
    cash_balance: Decimal
    buying_power: Decimal
    equity: Decimal
    market_value: Decimal
    todays_profit_loss: Decimal
    uncleared_deposit: Decimal
    balance_detail: AccountBalanceDetail
    currency_details: list[AccountCurrencyDetail] | None = None
    commission: Decimal


class AccountError(TradestationModel):
    account_id: str = Field(alias="AccountID")
    error: str
    message: str


class AccountBalances(TradestationModel):
    balances: list[AccountBalance]
    errors: list[AccountError]


class Account(TradestationModel):
    account_detail: AccountDetail | None = None
    account_id: str = Field(alias="AccountID")
    account_type: str
    alias: str | None = None
    alt_id: str | None = Field(default=None, alias="AltID")
    currency: str
    status: str

    @classmethod
    def get_accounts(cls, session: Session) -> list[Self]:
        data = session._get("/brokerage/accounts")
        return [cls(**item) for item in data["Accounts"]]

    @classmethod
    async def a_get_accounts(cls, session: Session) -> list[Self]:
        data = await session._a_get("/brokerage/accounts")
        return [cls(**item) for item in data["Accounts"]]

    @classmethod
    def get_balances(cls, session: Session, accounts: list[Self]) -> AccountBalances:
        numbers = ",".join([a.account_id for a in accounts])
        data = session._get(f"/brokerage/accounts/{numbers}/balances")
        return AccountBalances(**data)

    @classmethod
    async def a_get_balances(
        cls, session: Session, accounts: list[Self]
    ) -> AccountBalances:
        numbers = ",".join([a.account_id for a in accounts])
        data = await session._a_get(f"/brokerage/accounts/{numbers}/balances")
        return AccountBalances(**data)
