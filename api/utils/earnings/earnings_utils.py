from datetime import datetime


class Earnings:

    @staticmethod
    def from_timestamp_to_utc_isoformat_br(timestamp: float):
        UTC_datetime_converted = datetime.utcfromtimestamp(timestamp).strftime(format="%Y-%m-%d")
        return UTC_datetime_converted
