from http import HTTPStatus

from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import ServiceException


class MoneyFlowPerformedOutsideTransactionWindow(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Money flow performed outside the transaction window"
        self.status_code = HTTPStatus.NOT_ACCEPTABLE
        self.internal_code = InternalCode.OUTSIDE_THE_OPERATION_WINDOW
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
