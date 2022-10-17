# Ebisu
from src.domain.exceptions.base_exceptions.model import TransportException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class ErrorSendingToBifrostClient(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error trying sending to bifrost queue"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_IN_BIFROST_CLIENT
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
