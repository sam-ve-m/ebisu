from abc import ABC, abstractmethod


class BaseBalance(ABC):

    @abstractmethod
    def has_balance(self):
        pass
