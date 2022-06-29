# STANDARD IMPORTS
from typing import List
from pydantic import BaseModel

# PROJECT IMPORTS
from src.domain.earning.base.response.model import EarningsTransactionBrResponse


# "paid_earnings": earnings_paid_values,
# "payable_earnings": earnings_payable_values,
# "record_date_earnings": earnings_record_date_values,

class EarningsRecordResponse(BaseModel):
    paid: List[EarningsTransactionBrResponse]
    payable: List[EarningsTransactionBrResponse]
    record_date: List[EarningsTransactionBrResponse]

class BrEarningsModelToResponse:

