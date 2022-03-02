from abc import ABC, abstractmethod
from typing import Optional


class IService(ABC):
    @abstractmethod
    async def get_service_response(self) -> Optional[dict]:
        pass
