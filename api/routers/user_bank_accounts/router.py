# from api.domain.enums.region import Region
# from fastapi import Request, APIRouter
#
# from api.services.get_balance.get_balance import GetBalance
# from api.services.jwt.service_jwt import JwtService
#
#
# class UserBankAccountsRouter:
#
#     __exchange_router = APIRouter()
#
#     @staticmethod
#     def get_exchange_router():
#         return ExchangeRouter.__exchange_router
#
#     @staticmethod
#     @__exchange_router.get("/balance", tags=["Balance"])
#     async def get_balance(region: Region, request: Request):
#         jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
#
#         balance = await GetBalance.get_service_response(region=region, jwt_data=jwt_data)
#         return balance
