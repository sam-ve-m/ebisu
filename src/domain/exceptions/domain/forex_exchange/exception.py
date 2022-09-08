# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import DomainException

# Standards
from http import HTTPStatus


class InvalidOperation(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid combination of base currency to quote currency"
        self.code = HTTPStatus.BAD_REQUEST
        super().__init__(self.msg, self.code, args, kwargs)


class SpreadTaxNotFound(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Spread data not found on customer"
        self.code = HTTPStatus.BAD_REQUEST
        super().__init__(self.msg, self.code, args, kwargs)


class OperationNotImplemented(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Nature of quote operation not implemented"
        self.code = HTTPStatus.BAD_REQUEST
        super().__init__(self.msg, self.code, args, kwargs)


class ErrorOnValidateExchangeSimulationProposalData(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to validate the customer exchange simulation proposal"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)
