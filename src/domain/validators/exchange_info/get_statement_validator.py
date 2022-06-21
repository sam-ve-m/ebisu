from typing import Optional

from pydantic import BaseModel
from src.domain.enums.statement_type import StatementType


class GetBrStatementModel(BaseModel):
    statement_type: StatementType
    limit: int
    offset: int


class GetUsStatementModel(BaseModel):
    statement_type: StatementType
    limit: int
    offset: Optional[int]
