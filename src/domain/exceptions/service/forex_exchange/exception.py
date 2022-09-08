# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import ServiceException

# Standards
from http import HTTPStatus


class ErrorOnGetCustomerQuotationToken(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error on get customer quotation token"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)


class ErrorOnGetExchangeSimulationProposal(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get exchange simulation proposal from customer"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)


class CustomerQuotationTokenNotFound(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer quotation token value not found"
        self.code = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(self.msg, self.code, args, kwargs)

