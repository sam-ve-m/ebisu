from pydantic import BaseModel
from src.domain.enums.region import Region


class AccountCloseStepsRequest(BaseModel):
    region: Region
