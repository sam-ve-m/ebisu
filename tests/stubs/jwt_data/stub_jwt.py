payload_data_stub = {
    "exp": 1678209788,
    "created_at": 1646673788.442139,
    "scope": {
        "view_type": "default",
        "user_level": "client",
        "features": [
            "default",
            "realtime"
        ]
    },
    "user": {
        "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
        "nick_name": "RAST3",
        "portfolios": {
            "br": {
                "bovespa_account": "000000014-6",
                "bmf_account": "14"
            },
            "us": {
                "_": None
            }
        },
        "client_has_br_trade_allowed": False,
        "client_has_us_trade_allowed": False,
        "client_profile": "investor"
    }
}

user_jwt_stub = {
        "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
        "nick_name": "RAST3",
        "portfolios": {
            "br": {
                "bovespa_account": "000000014-6",
                "bmf_account": "14"
            },
            "us": {
                "_": None
            }
        },
        "client_has_br_trade_allowed": False,
        "client_has_us_trade_allowed": False,
        "client_profile": "investor"
    }

balance_response_stub_br = {'region': 'BR'}
balance_payload_stub_br = {"payload": {"balance": 47499394.54}}

balance_response_stub_us = {'region': 'US'}
balance_payload_stub_us = {"payload": {"balance": 47499394.54}}


class StubRequestObj:
    def __init__(self, status_code=None):
        self.status_code = status_code

    @staticmethod
    def json():
        return payload_data_stub
