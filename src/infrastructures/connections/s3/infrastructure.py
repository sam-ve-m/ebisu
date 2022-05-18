import boto3

from src.infrastructures.env_config import config
from etria_logger import Gladsheim


class S3Infrastructure:
    @staticmethod
    def get_connection():
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                region_name=config("REGION_NAME"),
            )
            return s3_client
        except Exception as exception:
            Gladsheim.error(
                message=f"""S3Infrastructure::get_connection::Error on making connection with AWS
                "s3",
                aws_access_key_id={config("AWS_ACCESS_KEY_ID")},
                region_name={config("REGION_NAME")}:
                {exception}""",
                error=exception,
            )
