from pydantic import BaseModel
from api.domain.enums.region import Region


class StatementPdf(BaseModel):
    region: Region
