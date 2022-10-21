from src.domain.enums.response.internal_code import InternalCode
from src.domain.exceptions.base_exceptions.model import ServiceException
from http import HTTPStatus


class AccountCloseStepsForbidden(ServiceException):

    def __init__(self, *args, **kwargs):
        self.msg = "User is authorized but not has properties to access account close steps"
        self.status_code = HTTPStatus.FORBIDDEN
        self.internal_code = InternalCode.UNAUTHORIZED
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
