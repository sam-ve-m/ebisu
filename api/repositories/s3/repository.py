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
