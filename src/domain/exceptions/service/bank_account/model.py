from src.domain.enums.response.internal_code import InternalCode
from http import HTTPStatus

from src.domain.exceptions.base_exceptions.model import ServiceException


class BankAccountAlreadyExists(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Bank account already exists"
        self.status_code = HTTPStatus.OK
        self.internal_code = InternalCode.DATA_ALREADY_EXISTS
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class BankAccountNotExists(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Bank account not exists"
        self.status_code = HTTPStatus.OK
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
