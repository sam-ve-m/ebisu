from http import HTTPStatus
from aiohttp import ClientSession
from etria_logger import Gladsheim
from src.infrastructures.env_config import config


class DeviceSecurity:

    @staticmethod
    async def _execute_post(url: str, body: dict):
        try:
            async with ClientSession() as http_session:
                request_result = await http_session.post(url, json=body)
                return request_result
        except Exception as error:
            Gladsheim.error(
                error,
                message="Error executing post in device_info intern api",
            )
            raise

    @staticmethod
    async def decrypt_device_info(device_info: str) -> dict:
        body = {"deviceInfo": device_info}
        request_result = await DeviceSecurity._execute_post(
            config("DEVICE_SECURITY_DECRYPT_DEVICE_INFO_URL"), body
        )
        if not request_result.status == HTTPStatus.OK:
            Gladsheim.error(
                message="Error while decrypting device info",
                status=request_result.status,
                content=request_result.content
            )
            raise
        json_response = await request_result.json()
        device_info_decrypted = (
            json_response.get("deviceInfo")
        )
        return device_info_decrypted

    @staticmethod
    async def generate_device_id(device_info: str) -> str:
        body = {"deviceInfo": device_info}
        request_result = await DeviceSecurity._execute_post(
            config("DEVICE_SECURITY_DEVICE_ID_URL"), body
        )
        if not request_result.status == HTTPStatus.OK:
            Gladsheim.error(
                message="Error while generating device_id",
                status=request_result.status,
                content=request_result.content
            )
            raise
        json_response = await request_result.json()
        device_id = (
            json_response.get("deviceID")
        )
        return device_id
