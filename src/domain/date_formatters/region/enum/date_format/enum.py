from enum import Enum


class RegionDateFormat(Enum):
    BR_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    BR_DATE_ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"
    US_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
