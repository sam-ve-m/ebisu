from datetime import datetime
import datetime


class Earnings:

    @staticmethod
    def from_timestamp_to_utc_isoformat_br(timestamp: float):
        raw_format_date = datetime.fromtimestamp(timestamp / 1000)
        format_date = raw_format_date.strftime(format="%Y-%m-%d")
        return format_date
