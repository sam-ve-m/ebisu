class IntegrityJwtError(Exception):
    def __init__(
        self, msg="The JWT is Invalid or has expired (Integrity Error)", *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class AuthenticationJwtError(Exception):
    def __init__(
        self,
        msg="The JWT is Invalid or has expired (Authentication Error)",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class DataNotFoundError(Exception):
    def __init__(self, msg="The Data Was Not Found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class NoPathFoundError(Exception):
    def __init__(self, msg="The Path Was Not Found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class NoPdfFoundError(Exception):
    def __init__(self, msg="Broker note not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MoneyFlowResolverNoFoundError(Exception):
    def __init__(self, msg="Error to resolver money flow", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class InvalidAccountsOwnership(Exception):
    def __init__(self, msg="Invalid accounts ownership", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MoneyFlowPerformedOutsideTransactionWindow(Exception):
    def __init__(self, msg="Money flow performed outside the transaction window", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class UnableToProcessMoneyFlow(Exception):
    def __init__(self, msg="Unable to process money flow", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class NotMappedCurrency(Exception):
    def __init__(
        self,
        msg="Unable to process money flow, because currency is not mapped",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class InvalidElectronicaSignature(Exception):
    def __init__(self, msg="Invalid electronica signature", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class FailToSaveAuditingTrail(Exception):
    def __init__(self, msg="Fail to save auditing trail", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class FailToGetDataFromTransportLayer(Exception):
    def __init__(self, msg="Fail to get data from transport layer", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class ForbiddenError(Exception):
    def __init__(self, msg="Forbidden", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class BadRequestError(Exception):
    def __init__(self, msg="Bad request", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class InternalServerError(Exception):
    def __init__(self, msg="Internal server", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class UnauthorizedError(Exception):
    def __init__(self, msg="Unauthorized", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
