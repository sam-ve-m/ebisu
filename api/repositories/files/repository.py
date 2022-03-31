from datetime import datetime
from typing import List

from api.infrastructures.connections.s3.infrastructure import S3Infrastructure
from api.infrastructures.env_config import config


class FileRepository:

    _bucket_name = config("AWS_FILE_BUCKET_NAME")
    URL_LINK_EXPIRE_SECONDS = 30
    infra = S3Infrastructure
    client = None

    @classmethod
    def _get_client(cls):
        if cls.client is None:
            cls.client = cls.infra.get_connection()
        return cls.client

    @classmethod
    def generate_file_link(cls, file_path: str):
        s3_client = cls._get_client()
        link = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": cls._bucket_name,
                "Key": file_path,
            },
            ExpiresIn=cls.URL_LINK_EXPIRE_SECONDS,
        )
        return link

    @classmethod
    def list_all_directories_in_path(cls, file_path: str) -> List[str]:
        s3_client = cls._get_client()
        directories = s3_client.list_objects(
            Bucket=cls._bucket_name, Prefix=file_path, Delimiter="/"
        )
        if not directories:
            return []
        return directories

    @classmethod
    def upload_file(cls, file_path: str, content, expire_date: datetime):
        s3_client = cls._get_client()
        files_upload = s3_client.put_object(
            Bucket=cls._bucket_name,
            Key=file_path,
            Body=content,
            ContentType="application/pdf",
            Expires=expire_date,
        )
        return files_upload
