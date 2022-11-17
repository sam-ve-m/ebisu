# Ebisu
from src.domain.exceptions.base_exceptions.model import DomainException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class DataNotFoundInJwt(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get some value in jwt_data"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_VALIDATION_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class BrAccountIsBlocked(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Brazilian account is blocked"
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.ACCOUNT_BR_IS_BLOCKED
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
