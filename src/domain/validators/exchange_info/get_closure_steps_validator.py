from pydantic import BaseModel
from src.domain.enums.region import Region


class ClosureStepsModel(BaseModel):
    region: Region
