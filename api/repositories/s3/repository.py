from datetime import datetime
from typing import List

from api.utils.env_config import config


class S3Repository:

    _bucket_name = config("AWS_FILE_BUCKET_NAME")
    URL_LINK_EXPIRE_SECONDS = 30

    def __init__(self, infra):
        self.s3_client = infra

    def generate_file_link(self, file_path: str):
        link = self.s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self._bucket_name,
                "Key": file_path,
            },
            ExpiresIn=self.URL_LINK_EXPIRE_SECONDS,
        )
        return link

    def list_all_directories_in_path(self, file_path: str) -> List[str]:
        directories = self.s3_client.list_objects(
                Bucket=self._bucket_name,
                Prefix=file_path,
                Delimiter='/'
        )
        return directories

    def upload_file(self, file_path: str, content, expire_date: datetime):
        return self.s3_client.put_object(
            Bucket=self._bucket_name,
            Key=file_path,
            Body=content,
            ContentType="application/pdf",
            Expires=expire_date
        )
