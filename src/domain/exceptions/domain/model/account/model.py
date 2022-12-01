from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import DomainException
from http import HTTPStatus


class InvalidAccountsOwnership(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Opening hours for currency exchange operations are from 9:00 am to 4:30 pm."
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.INVALID_PARAMS
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class NotMappedCurrency(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Unable to process money flow, because currency is not mapped"
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.INVALID_PARAMS
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
