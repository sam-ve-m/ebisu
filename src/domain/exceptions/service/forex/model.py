# Ebisu
from src.domain.exceptions.base_exceptions.model import ServiceException
from src.domain.enums.response.internal_code import InternalCode

# Standards
from http import HTTPStatus


class CaronteCantFindToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error on Caronte trying to get company or customer token"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_IN_CARONTE
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class CustomerQuotationTokenNotFound(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer quotation token value not found"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
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

class InconsistentResultInRoute21(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = (
            "Different or invalid content than expected from route 21 in OuroInvest API"
        )
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


class InconsistentResultInRoute22(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = (
            "Different or invalid content than expected from route 22 in OuroInvest API"
        )
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


class InconsistentResultInRoute23(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = (
            "Different or invalid content than expected from route 23 in OuroInvest API"
        )
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


class DroppedToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "A new token was probably generated outside the application"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DROPPED_TOKEN
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class ErrorTryingToGetUniqueId(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error trying to get unique_id from jwt_data"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
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


class ExpiredToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Exceeded time limit to execute foreign exchange transaction"
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.EXPIRED_TOKEN
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class ErrorTryingToLockResource(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to lock resource in redis"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_IN_HALBERD
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class ErrorTryingToUnlock(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to unlock resource in redis"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_IN_HALBERD
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class InvalidToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid token. This is not a valid jwt."
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.JWT_INVALID
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class InsufficientFunds(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer does not have enough balance to complete the transaction"
        self.status_code = HTTPStatus.OK
        self.internal_code = InternalCode.INSUFFICIENT_FUNDS
        self.success = True
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class UnexpectedErrorInExchangeAPI(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error trying to get/post some resource from ExchangeAPI"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.INTERNAL_SERVER_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class ErrorTryingToDecodeJwt(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error to decode OuroInvest JWT. it's probably expired"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.JWT_INVALID
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
