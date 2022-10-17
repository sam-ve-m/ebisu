from pydantic import BaseModel
from src.domain.enums.region import Region


class StatementPdf(BaseModel):
    region: Region
