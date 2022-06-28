unique_id_stub = "40db7fee-6d60-4d73-824f-1bf87edc4491"

find_one_response_stub = {
    "portfolios": {
        "default": {
            "br": {"bovespa_account": "000000014-6", "bmf_account": "14"},
            "us": {
                "dw_id": "89c69304-018a-40b7-be5b-2121c16e109e",
                "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
            },
        },
        "vnc": {
            "br": [
                {"bovespa_account": "000000071-5", "bmf_account": "71"},
                {"bovespa_account": "000000018-9", "bmf_account": "18"},
            ]
        },
    }
}

find_one_by_region_stub = {
    "portfolios": {
        "default": {"br": {"bovespa_account": "000000014-6", "bmf_account": "14"}},
        "vnc": {
            "br": [
                {"bovespa_account": "000000071-5", "bmf_account": "71"},
                {"bovespa_account": "000000018-9", "bmf_account": "18"},
            ]
        },
    }
}

find_one_by_type_stub = {
    "portfolios": {
        "vnc": {
            "br": [
                {"bovespa_account": "000000071-5", "bmf_account": "71"},
                {"bovespa_account": "000000018-9", "bmf_account": "18"},
            ]
        }
    }
}

find_one_by_type_and_region = {
    "br": [
        {"bovespa_account": "000000071-5", "bmf_account": "71"},
        {"bovespa_account": "000000018-9", "bmf_account": "18"},
    ]
}
