# Third part
from aiokafka import AIOKafkaProducer

from src.infrastructures.env_config import config


class KafkaInfrastructure:

    producer = None

    @classmethod
    async def get_or_create_producer(cls):
        if cls.producer is None:
            cls.producer = AIOKafkaProducer(
                bootstrap_servers=config("BIFROST_KAFKA")
            )
            await cls.producer.start()

        return cls.producer
