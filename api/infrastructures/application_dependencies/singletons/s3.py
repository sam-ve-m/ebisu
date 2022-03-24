from api.infrastructures.connections.s3.infrastructure import S3Infrastructure
from api.repositories.s3.repository import S3Repository

from etria_logger import Gladsheim


class S3SingletonInstance:

    s3_singleton_instance = None

    @classmethod
    def get_s3_singleton_instance(cls):
        if cls.s3_singleton_instance is None:
            try:
                infra = S3Infrastructure.get_connection()
                cls.s3_singleton_instance = S3Repository(infra)
            except Exception as exception:
                Gladsheim.error(
                    message=f"""S3SingletonInstance::get_s3_singleton_instance::Error on S3 Infra: {exception}""",
                    error=exception,
                )

        return cls.s3_singleton_instance
