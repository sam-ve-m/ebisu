from dataclasses import dataclass


@dataclass
class DeviceInfo:
    decrypted_device_info: dict
    device_id: str
