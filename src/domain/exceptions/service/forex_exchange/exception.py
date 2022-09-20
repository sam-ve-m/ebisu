# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import ServiceException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class CaronteCantFindToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error on Caronte trying to get company or customer token"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_IN_CARONTE
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class CustomerQuotationTokenNotFound(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer quotation token value not found"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class DroppedToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "A new token was probably generated outside the application"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DROPPED_TOKEN
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class ExpiredToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Exceeded time limit to execute foreign exchange transaction"
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.EXPIRED_TOKEN
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class InvalidToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid token. This is not a valid jwt."
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.JWT_INVALID
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)


class UnexpectedErrorWhenTryingToGetExchangeSimulationProposal(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get exchange simulation proposal from customer"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.INTERNAL_SERVER_ERROR
        self.success = False
        super().__init__(self.msg, self.status_code, self.internal_code, self.success, args, kwargs)
