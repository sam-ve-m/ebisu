jwt_data_dummy = {
    "x-thebes-answer": {
        "exp": 1678209788,
        "created_at": 1646673788.442139,
        "scope": {
            "view_type": "default",
            "user_level": "client",
            "features": ["default", "realtime"],
        },
        "user": {
            "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
            "nick_name": "RAST3",
            "portfolios": {
                "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
                "us": {"_": None},
            },
            "client_has_br_trade_allowed": False,
            "client_has_us_trade_allowed": False,
            "client_profile": "investor",
        },
    }
}

jwt_data_to_create_account = {
    "exp": 1678209788,
    "created_at": 1646673788.442139,
    "scope": {
        "view_type": "default",
        "user_level": "client",
        "features": ["default", "realtime"],
    },
    "user": {
        "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
        "nick_name": "RAST3",
        "portfolios": {
            "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
            "us": {"_": None},
        },
        "client_has_br_trade_allowed": False,
        "client_has_us_trade_allowed": False,
        "client_profile": "investor",
    },
}

jwt_data_mist = {
    "unique_id": "2f962bf1-8d29-4363-87a0-0e9640b6e7b5",
    "device_identifier": "df9cf8cd-2bff-4c52-b7ac-123b2064cd3e",
    "exp": 1650805214,
}

jwt_with_bank_account_to_update = {
    "x-thebes-answer": {
        "exp": 1678209788,
        "created_at": 1646673788.442139,
        "scope": {
            "view_type": "default",
            "user_level": "client",
            "features": ["default", "realtime"],
        },
        "user": {
            "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
            "nick_name": "RAST3",
            "portfolios": {
                "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
                "us": {"_": None},
            },
            "client_has_br_trade_allowed": False,
            "client_has_us_trade_allowed": False,
            "client_profile": "investor",
        },
    },
    "bank_account": {
        "bank": "070",
        "account_type": "903984",
        "agency": "008956",
        "account_number": "000000020-6",
        "account_name": "poupança",
        "id": "ff302d01-849c-4805-b754-c1636cbbb1f3",
    },
}

jwt_with_bank_account_to_delete = {
    "x-thebes-answer": {
        "exp": 1678209788,
        "created_at": 1646673788.442139,
        "scope": {
            "view_type": "default",
            "user_level": "client",
            "features": ["default", "realtime"],
        },
        "user": {
            "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
            "nick_name": "RAST3",
            "portfolios": {
                "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
                "us": {"_": None},
            },
            "client_has_br_trade_allowed": False,
            "client_has_us_trade_allowed": False,
            "client_profile": "investor",
        },
    },
    "bank_account": {"id": "ff302d01-849c-4805-b754-c1636cbbb1f3"},
}

jwt_with_bank_account_to_create = {
    "x-thebes-answer": {
        "exp": 1678209788,
        "created_at": 1646673788.442139,
        "scope": {
            "view_type": "default",
            "user_level": "client",
            "features": ["default", "realtime"],
        },
        "user": {
            "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
            "nick_name": "RAST3",
            "portfolios": {
                "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
                "us": {"_": None},
            },
            "client_has_br_trade_allowed": False,
            "client_has_us_trade_allowed": False,
            "client_profile": "investor",
        },
    },
    "bank_account": {
        "bank": "070",
        "account_type": "8478674",
        "agency": "6255373",
        "account_number": "72655343-2",
        "account_name": "corrente",
        "cpf": "58038116020",
        "device_info": {
                "device_name": "iphone",
                "device_model": "13",
                "is_emulator": True,
                "device_operating_system_name": "IOS",
                "os_sdk_version": "45125",
                "device_is_in_root_mode": True,
                "device_network_interfaces": "hahahaha",
                "public_ip": "1548455475221",
                "access_ip": "0000145455545",
                "phone_wifi_ip": "123255444456",
                "geolocation": "Brasil, São Paulo, SP"
        }
    },
}

jwt_with_bank_account_to_create_invalid = {
    "x-thebes-answer": {
        "exp": 1678209788,
        "created_at": 1646673788.442139,
        "scope": {
            "view_type": "default",
            "user_level": "client",
            "features": ["default", "realtime"],
        },
        "user": {
            "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
            "nick_name": "RAST3",
            "portfolios": {
                "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
                "us": {"_": None},
            },
            "client_has_br_trade_allowed": False,
            "client_has_us_trade_allowed": False,
            "client_profile": "investor",
        },
    },
    "bank_account": {
        "bank": "1234556",
        "account_type": "8478674",
        "agency": "6255373",
        "account_number": "72655343-2",
        "account_name": "corrente",
        "cpf": "58038116020",
    },
}

get_accounts_dummy = {
    "bank_accounts": [
        {
            "bank": "648498574893",
            "account_type": "903984",
            "agency": "0087565",
            "account_number": "000000014-6",
            "account_name": "corrente",
            "id": "ff302d01-849c-4805-b754-c1636cbbb1f3",
            "status": "active",
        },
        {
            "bank": "789456123",
            "account_type": "123456",
            "agency": "00321654",
            "account_number": "000000666-1",
            "account_name": "corrente teste",
            "id": "15f11e59-4d44-4939-9bf0-25c1501e3b5d",
            "status": "active",
        },
    ]
}

find_all_response_dummy = [
    {
        "bank_accounts": [
            {
                "bank": "789456123",
                "account_type": "123456",
                "agency": "00321654",
                "account_number": "000000666-1",
                "account_name": "corrente teste",
                "id": "15f11e59-4d44-4939-9bf0-25c1501e3b5d",
                "status": "active",
            }
        ]
    }
]

find_one_response_dummy = {
    "bank": "789456123",
    "account_type": "123456",
    "agency": "00321654",
    "account_number": "000000666-1",
    "account_name": "corrente teste",
    "id": "15f11e59-4d44-4939-9bf0-25c1501e3b5d",
    "status": "active",
}
find_one_wrong_response_dummy = {
    "bank": None,
    "account_type": None,
    "agency": None,
    "account_number": None,
    "status": "deactivated",
    "id": None,
}
find_one_response_with_cpf_dummy = {
    "bank": "789456123",
    "cpf": "58038116020",
    "account_type": "123456",
    "agency": "00321654",
    "account_number": "000000666-1",
    "account_name": "corrente teste",
    "id": "15f11e59-4d44-4939-9bf0-25c1501e3b5d",
    "status": "active",
}

request_bank_account_dummy = {
    "unique_id": "15f11e59-4d44-4939-9bf0-25c1501e3b5d",
    "bank_accounts": {
        "bank": "789456123",
        "account_type": "123456",
        "agency": "00321654",
        "account_number": "000000666-1",
        "account_name": "corrente teste",
        "status": "active",
    },
}

user_from_client_stub = {
    "cpf": "58038116020",
    "bank": "725344232627826",
    "account_type": "837746545453",
    "agency": "0000005343",
    "account_number": "99927276253-2",
    "account_name": "corrente",
}
user_from_client_2_stub = {
    "cpf": None,
    "bank": None,
    "account_type": None,
    "agency": "0000005343",
    "account_number": "99927276253-2",
    "account_name": "corrente",
}

stock_portfolios_response_dummy = {
    "default": {
        "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
        "us": {
            "dw_id": "89c69304-018a-40b7-be5b-2121c16e109e",
            "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
        },
    },
    "vnc_portfolios": {
        "br": [
            {"bovespa_account": "000000071-5", "bmf_account": "71"},
            {"bovespa_account": "000000018-9", "bmf_account": "18"},
        ]
    },
}
