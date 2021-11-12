from pydantic import BaseModel


class CustomerParams(BaseModel):
    bmf_account: int
    symbols: str
    order_type: str
    order_status: str
    trade_sides: str
    time_in_forces: str
