from pydantic import BaseModel


class BmfAccount(BaseModel):
    bmf_account: int


class Symbols(BaseModel):
    symbols: str


class OrderType(BaseModel):
    order_type: str


class OrderStatus(BaseModel):
    order_status: str


class TradeSides(BaseModel):
    trade_sides: str


class TimeInForces(BaseModel):
    time_in_forces: str


class SearchParams(BmfAccount, Symbols, OrderType, OrderStatus, TradeSides, TimeInForces):
    pass
