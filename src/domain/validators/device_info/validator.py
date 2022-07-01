from pydantic import BaseModel


class DeviceInformationOptional(BaseModel):
    device_name: str = None
    device_model: str = None
    is_emulator: bool = None
    device_operating_system_name: str = None
    os_sdk_version: str = None
    device_is_in_root_mode: bool = None
    device_network_interfaces: str = None
    public_ip: str = None
    access_ip: str = None
    phone_wifi_ip: str = None
    geolocation: str = None