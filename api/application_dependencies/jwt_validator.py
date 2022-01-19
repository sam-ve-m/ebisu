from typing import Optional

from fastapi import Header


def verify_jwt_token(
    x_thebs_answer: str = Header(..., title="customer token")
) -> Optional[Exception]:
    pass
