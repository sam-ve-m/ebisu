import boto3

from api.utils.env_config import config


class S3Infrastructure:
    @staticmethod
    def get_connection():
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
            region_name=config("REGION_NAME"),
        )
        return s3_client
