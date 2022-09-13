# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import ServiceException

# Standards
from http import HTTPStatus


class CaronteCantFindToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error on Caronte trying to get company or customer token"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)


class CustomerQuotationTokenNotFound(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer quotation token value not found"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)


class DroppedToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "A new token was probably generated outside the application"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)


class ExpiredToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Exceeded time limit to execute foreign exchange transaction"
        self.code = HTTPStatus.BAD_REQUEST
        super().__init__(self.msg, self.code, args, kwargs)


class InvalidToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid token. This is not a valid jwt."
        self.code = HTTPStatus.UNAUTHORIZED
        super().__init__(self.msg, self.code, args, kwargs)


class UnexpectedErrorWhenTryingToGetExchangeSimulationProposal(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get exchange simulation proposal from customer"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)
