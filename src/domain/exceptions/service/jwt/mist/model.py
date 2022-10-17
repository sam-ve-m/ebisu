# Ebisu
from src.domain.exceptions.base_exceptions.model import ServiceException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class InvalidElectronicSignature(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid electronica signature"
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.INVALID_SIGNATURE_ELECTRONIC
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
