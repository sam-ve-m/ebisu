from api.infrastructures.s3.infrastructure import S3Infrastructure
from api.repositories.s3.repository import S3Repository


class S3SingletonInstance:

    s3_singleton_instance = None

    @classmethod
    def get_s3_singleton_instance(cls):
        if cls.s3_singleton_instance is None:
            infra = S3Infrastructure.get_connection()
            cls.s3_singleton_instance = S3Repository(infra)

        return cls.s3_singleton_instance
