class IntegrityJwtError(Exception):
    def __init__(
        self,
        msg="The jwt is Invalid or has expired",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)


class AuthenticationJwtError(Exception):
    def __init__(
        self,
        msg="The jwt is Invalid or has expired",
        *args,
        **kwargs
    ):
        super().__init__(msg, *args, **kwargs)
        