import urllib.parse
from unittest.mock import MagicMock


# Stubs Oracle and AWS Connection
class StubS3Connection:
    S3_BUCKET = "BROKER_NOTE_BUCKET"

    @classmethod
    def get_s3(cls):
        return MagicMock()

    @classmethod
    def generate_presigned_url(cls, get_object, Params):
        url = "https://brokerage-note-and-bank-statement.s3.amazonaws.com/109/?"
        params = {'AWSAccessKeyId': '5243792748DGHDJDH',
                  'signature': 'FHDGKFU6356489nfhjd65243',
                  'expires': '875342628946'}
        url_parsed = (url + urllib.parse.urlencode(params))
        return url_parsed

    @classmethod
    def generate_file_link(cls, file_path):
        s3_client = cls.get_s3()
        link = cls.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": StubS3Connection.S3_BUCKET,
                "Key": file_path,
            }
        )
        if link is None:
            raise Exception
        return link


class StubOracleRepository:

    @classmethod
    def _get_connection(cls):
        return MagicMock()

    @classmethod
    def get_data(cls, sql: str = None):
        if not sql:
            return {}
        sql_query = {
            sql: [{"VL_TOTAL": 10000.41}]}
        rows = sql_query[sql][0]['VL_TOTAL']
        if not rows:
            return {}
        return rows


# Complete Dummy object of jwt requests
payload_data_dummy = {
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

# Dummy object of decripted jwt object getting the user
user_jwt_dummy = {
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

# Dummy object of decripted jwt - portfolios
portfolios_jwt_dummy = {
    "br": {
        "bovespa_account": "000000014-6",
        "bmf_account": "14"
    },
    "us": {
        "_": None
    }
}

balance_response_dummy_br = {'region': 'BR'}
balance_payload_dummy_br = {"payload": {"balance": 47499394.54}}

balance_response_dummy_us = {'region': 'US'}
balance_payload_dummy_us = {"payload": {"balance": 104993635.20}}
