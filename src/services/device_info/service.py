from fastapi import Request

from src.domain.models.device_info.dto import DeviceInfo
from src.transport.device_info.transport import DeviceSecurity


class DeviceInfoService:

    @staticmethod
    def __get_device_info_from_headers(request: Request) -> str:
        for header_tuple in request.headers.raw:
            if b"x-device-info" in header_tuple:
                device_info = header_tuple[1].decode()
                return device_info
        raise

    @staticmethod
    async def get_device_info(request: Request) -> DeviceInfo:
        device_info = DeviceInfoService.__get_device_info_from_headers(request)
        decrypted_device_info = await DeviceSecurity.decrypt_device_info(device_info)
        device_id = await DeviceSecurity.generate_device_id(device_info)
        device_info_dto = DeviceInfo(
            decrypted_device_info=decrypted_device_info,
            device_id=device_id
        )
        return device_info_dto
