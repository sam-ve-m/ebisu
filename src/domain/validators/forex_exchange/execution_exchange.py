# # Ebisu
# from src.domain.enums.forex_exchange.timezones_types import TimeZoneBr
# from src.domain.exceptions.domain.forex_exchange.exception import ClosedExchangeOperations
#
# # Standards
# from datetime import datetime, timezone, timedelta
#
# # Third party
# from pydantic import BaseModel, validator
# import pandas_market_calendars as exchange_calendar
#
#
# class ExchangeExecution(BaseModel):
#     customer_exchange_token: str
#     request_datetime: datetime = datetime.now(
#         tz=timezone(
#             offset=timedelta(
#                 hours=TimeZoneBr.BRAZILIAN.value
#             )
#         )
#     )
#
#     @validator("request_datetime")
#     def in_business_hours(cls, request_datetime: datetime):
#         request_datetime = int(request_datetime.strftime("%H%M"))
#         if not 859 < request_datetime < 1631:
#             raise ClosedExchangeOperations
#
#     @validator("request_datetime")
#     def in_business_day(cls, request_datetime: datetime):
#         datetime_formated = request_datetime.strftime("%Y-%M-%d")
#         bmf_calendar = exchange_calendar.get_calendar("BMF")
#         nyse_calender = exchange_calendar.get_calendar("NYSE")
#         bmf_valid_day =
#         intersection_calendar =''
#         if day_number not in [0, 1, 2, 3, 4]:
#             raise ClosedExchangeOperations
