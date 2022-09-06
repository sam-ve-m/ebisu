# Ebisu
from src.domain.exceptions.base_exceptions.exceptions import ServiceException


class UserTokenNotFound(ServiceException):
    pass


class InvalidOperation(ServiceException):
    pass


class ErrorOnGetUserToken(ServiceException):
    pass


class ErrorOnGetExchangeSimulationProposal(ServiceException):
    pass
