from abc import ABC, abstractmethod

class IBankTransfer(ABC):
  
  @abstractmethod
  @staticmethod
  def get_bank_transfer_account():
    pass