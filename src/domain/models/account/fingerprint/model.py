from typing import NewType, Tuple
from src.domain.enums.region import Region

IsPrimaryAccount = NewType("IsPrimaryAccount", bool)
Fingerprint = Tuple[Region, IsPrimaryAccount]
