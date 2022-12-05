from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import ServiceException
from http import HTTPStatus


class MarketOptionNotImplemented(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "This market option has no implemented broker note."
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
