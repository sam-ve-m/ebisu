from pydantic import BaseModel
from src.domain.enums.region import Region
from src.domain.enums.statement_type import StatementType


class GetStatementModel(BaseModel):
    statement_type: StatementType
    region: Region
    limit: int
    offset: int
