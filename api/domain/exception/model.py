class IntegrityJwtError(Exception):
    def __init__(
        self,
        msg="The JWT is Invalid or has expired (Integrity Error)",
        *args,
        **kwargs
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
    def __init__(
        self,
        msg="The Data Was Not Found",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class NoPathFoundError(Exception):
    def __init__(
        self,
        msg="The Path Was Not Found",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class NoPdfFoundError(Exception):
    def __init__(
        self,
        msg="Broker note not found",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)
