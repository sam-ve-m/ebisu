class InvalidAccountsOwnership(Exception):
    def __init__(self, msg="Invalid accounts ownership", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MoneyFlowPerformedOutsideTransactionWindow(Exception):
    def __init__(
        self, msg="Money flow performed outside the transaction window", *args, **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class NotMappedCurrency(Exception):
    def __init__(
        self,
        msg="Unable to process money flow, because currency is not mapped",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class FailToSaveAuditingTrail(Exception):
    def __init__(self, msg="Fail to save auditing trail", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class FailToGetDataFromTransportLayer(Exception):
    def __init__(self, msg="Fail to get data from transport layer", *args, **kwargs):
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
