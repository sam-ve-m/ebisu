from datetime import datetime


class Earnings:
    @staticmethod
    def from_timestamp_to_utc_isoformat_br(timestamp: float):
        timestamp_miliseconds = timestamp / 1000
        raw_date = datetime.fromtimestamp(timestamp_miliseconds)
        format_date = raw_date.strftime("%Y-%m-%d")
        return format_date
