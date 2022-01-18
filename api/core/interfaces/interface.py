from abc import ABC, abstractmethod
from typing import Optional


class IService(ABC):
    @abstractmethod
    def get_service_response(self) -> Optional[dict]:
        pass
