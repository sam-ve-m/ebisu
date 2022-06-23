from typing import Optional

from pydantic import BaseModel, Field
from src.domain.enums.statement_type import StatementType


class GetBrStatement(BaseModel):
    statement_type: StatementType
    limit: int
    offset: int


class GetUsStatement(BaseModel):
    statement_type: StatementType
    limit: int = Field(gt=0)
    offset: Optional[int]
