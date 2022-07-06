# PROJECT IMPORTS
from src.domain.date_formatters.region.date_time.model import RegionStringDateTime
from src.domain.date_formatters.region.enum.date_format.enum import RegionDateFormat
from src.domain.earning.us.model import Earning


get_transactions_stub = [
    {
        "dividend": {
            "type": "CASH",
            "amountPerShare": 0.1511,
            "taxCode": "FULLY_TAXABLE",
        },
        "instrument": {
            "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
            "symbol": "AAPL",
            "name": "PowerShares S&P 500 High Div Low Vol ETF",
        },
        "tranWhen": "2019-06-03T15:12:00.345Z",
    }
]

earnings_transaction_stub = {
    "dividend": {"type": "CASH", "amountPerShare": 0.1511, "taxCode": "FULLY_TAXABLE"},
    "instrument": {
        "id": "9563a550-9f3b-47aa-b570-f18435f218d2",
        "symbol": "AAPL",
        "name": "PowerShares S&P 500 High Div Low Vol ETF",
    },
    "tranWhen": "2019-06-03T15:12:00.345Z",
}

get_transactions_model_stub = Earning(
    **{
        "symbol": "AAPL",
        "description": "PowerShares S&P 500 High Div Low Vol ETF",
        "amount_per_share": 0.1511,
        "date": RegionStringDateTime(
            "2019-06-03T15:12:00.345Z", RegionDateFormat.US_DATE_FORMAT
        ),
    }
)
