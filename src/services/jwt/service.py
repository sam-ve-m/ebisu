# STANDARD LIBS
from typing import Optional
from etria_logger import Gladsheim

# OUTSIDE LIBRARIES
from fastapi import Request
from jwt import JWT

from heimdall_client import Heimdall, HeimdallStatusResponses
from mist_client import Mist, MistStatusResponses
from src.domain.exceptions.service.jwt.thebes_answer.model import InvalidJwt
from src.domain.exceptions.service.jwt.mist.model import InvalidElectronicSignature


class JwtService:

    instance = JWT()
    heimdall = Heimdall
    mist = Mist

    @staticmethod
    def __get_mist_from_request(request: Request):
        mist_token = None
        for header_tuple in request.headers.raw:
            if b"x-mist" in header_tuple:
                mist_token = header_tuple[1].decode()
                break
        return mist_token

    @staticmethod
    async def validate_mist(request: Request, user_data: dict) -> bool:
        mist_token = JwtService.__get_mist_from_request(request=request)
        is_valid = await JwtService.mist.validate_jwt(jwt=mist_token)
        mist_content, status = await JwtService.mist.decode_payload(jwt=mist_token)
        if (
            is_valid
            and status == MistStatusResponses.SUCCESS
            and user_data["unique_id"] == mist_content["decoded_jwt"]["unique_id"]
        ):
            return True
        raise InvalidElectronicSignature()

    @staticmethod
    def __get_thebes_answer_from_request(request: Request):
        thebes_answer = None
        for header_tuple in request.headers.raw:
            if b"x-thebes-answer" in header_tuple:
                thebes_answer = header_tuple[1].decode()
                break
        return thebes_answer

    @classmethod
    async def __decode_thebes_answer(cls, encrypted_payload: str) -> Optional[dict]:
        payload, status = await cls.heimdall.decode_payload(jwt=encrypted_payload)
        if status != HeimdallStatusResponses.SUCCESS:
            Gladsheim.error(message=str(payload))
            # TODO: mapear erros do heimdall para ebisu
            raise InvalidJwt()
        return payload["decoded_jwt"]

    @classmethod
    async def validate_and_decode_thebes_answer(cls, request: Request) -> dict:
        jwt = JwtService.__get_thebes_answer_from_request(request=request)
        if jwt is None:
            raise InvalidJwt()
        decoded_jwt = dict(await cls.__decode_thebes_answer(jwt))
        return decoded_jwt
