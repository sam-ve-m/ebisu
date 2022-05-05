jwt_data_dummy = {'x-thebes-answer': {'exp': 1678209788, 'created_at': 1646673788.442139, 'scope': {'view_type': 'default', 'user_level': 'client', 'features': ['default', 'realtime']}, 'user': {'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491', 'nick_name': 'RAST3', 'portfolios': {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'}, 'us': {'_': None}}, 'client_has_br_trade_allowed': False, 'client_has_us_trade_allowed': False, 'client_profile': 'investor'}}}


jwt_data_mist = {
      "unique_id": "2f962bf1-8d29-4363-87a0-0e9640b6e7b5",
      "device_identifier": "df9cf8cd-2bff-4c52-b7ac-123b2064cd3e",
      "exp": 1650805214
    }

jwt_with_bank_account_to_update = {'x-thebes-answer': {'exp': 1678209788, 'created_at': 1646673788.442139, 'scope': {'view_type': 'default', 'user_level': 'client', 'features': ['default', 'realtime']}, 'user': {'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491', 'nick_name': 'RAST3', 'portfolios': {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'}, 'us': {'_': None}}, 'client_has_br_trade_allowed': False, 'client_has_us_trade_allowed': False, 'client_profile': 'investor'}}, 'bank_account': {'bank': '6484976383936', 'account_type': '903984', 'agency': '008956', 'account_number': '000000020-6', 'account_name': 'poupança', 'id': 'ff302d01-849c-4805-b754-c1636cbbb1f3'}}

jwt_with_bank_account_to_delete = {'x-thebes-answer': {'exp': 1678209788, 'created_at': 1646673788.442139, 'scope': {'view_type': 'default', 'user_level': 'client', 'features': ['default', 'realtime']}, 'user': {'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491', 'nick_name': 'RAST3', 'portfolios': {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'}, 'us': {'_': None}}, 'client_has_br_trade_allowed': False, 'client_has_us_trade_allowed': False, 'client_profile': 'investor'}}, 'bank_account': {'id': 'ff302d01-849c-4805-b754-c1636cbbb1f3'}}

jwt_with_bank_account_to_create = {'x-thebes-answer': {'exp': 1678209788, 'created_at': 1646673788.442139, 'scope': {'view_type': 'default', 'user_level': 'client', 'features': ['default', 'realtime']}, 'user': {'unique_id': '40db7fee-6d60-4d73-824f-1bf87edc4491', 'nick_name': 'RAST3', 'portfolios': {'br': {'bovespa_account': '000000014-6', 'bmf_account': '14'}, 'us': {'_': None}}, 'client_has_br_trade_allowed': False, 'client_has_us_trade_allowed': False, 'client_profile': 'investor'}}, 'bank_account': {"bank": "26544382992763", "account_type": "8478674", "agency": "6255373", "account_number": "72655343-2", "account_name": "corrente", "cpf":"58038116020"}}

get_accounts_dummy = {
    "bank_accounts": [
        {
            "bank": "648498574893",
            "account_type": "903984",
            "agency": "0087565",
            "account_number": "000000014-6",
            "account_name": "corrente",
            "id": "ff302d01-849c-4805-b754-c1636cbbb1f3",
            "status": "active"
        },
        {
            "bank": "789456123",
            "account_type": "123456",
            "agency": "00321654",
            "account_number": "000000666-1",
            "account_name": "corrente teste",
            "id": "15f11e59-4d44-4939-9bf0-25c1501e3b5d",
            "status": "active"
        }
    ] }

