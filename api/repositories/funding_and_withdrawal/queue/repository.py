from etria_logger import Gladsheim
from nidavellir import Sindri

from api.infrastructures.kafka.infraestructure import KafkaInfrastructure
from aiokafka.errors import KafkaTimeoutError, KafkaError
from json import dumps


class FundingAndWithdrawalRepository:

    infra = KafkaInfrastructure

    @classmethod
    async def send_to_bifrost(cls, topic: str, message: dict) -> bool:
        is_message_sent = False
        record_metadata = None

        try:
            kafka_producer = await cls.infra.get_or_create_producer()
            message = dumps(message, default=Sindri.dict_to_primitive_types)
            record_metadata = await kafka_producer.send_and_wait(topic=topic, value=message.encode())
            is_message_sent = True
        except KafkaTimeoutError as err:
            message = f"FundingAndWithdrawalRepository::send_to_persephone::KafkaTimeoutError::is_message_sent:{is_message_sent}::record metadata:{record_metadata}"
            Gladsheim.error(msg=message, stacklevel=err, exc_info=True)

        except KafkaError as err:
            message = f"FundingAndWithdrawalRepository::send_to_persephone::KafkaError::is_message_sent:{is_message_sent}::record metadata:{record_metadata}"
            Gladsheim.error(msg=message, stacklevel=err, exc_info=True)

        except Exception as err:
            message = f"FundingAndWithdrawalRepository::send_to_persephone::Exception::is_message_sent:{is_message_sent}::record metadata:{record_metadata}"
            Gladsheim.error(msg=message, stacklevel=err, exc_info=True)

        return is_message_sent
