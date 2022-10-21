from src.domain.exceptions.base_exceptions.model import TransportException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class FailToGetDataFromTransportLayer(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when access us partner api"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_IN_US_PARTNER
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
