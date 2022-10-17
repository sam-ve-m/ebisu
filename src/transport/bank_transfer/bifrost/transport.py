# Ebisu
from src.domain.enums.forex.operations import OperationType
from src.domain.exceptions.transport.forex.model import ErrorSendingToBifrostClient
from src.domain.models.forex.proposal.execution_request_data.model import ExecutionModel

# Third party
from bifrost_client import BifrostClient, BifrostTopics
from etria_logger import Gladsheim


class BankTransferBifrostTransport:
    ted_topic = BifrostTopics.TRANSFERS_BETWEEN_SINACOR_AND_EXTERNAL_BANK

    @classmethod
    async def send_transfer_message_to_bifrost(cls, message: dict) -> True:
        await cls._send_to_queue(message=message, topic=cls.ted_topic)

    @staticmethod
    async def _send_to_queue(message: dict, topic: BifrostTopics):
        success, bifrost_status = await BifrostClient.send_to_bifrost(
            message=message,
            topic=topic,
        )
        if not success:
            Gladsheim.error(
                bifrost_status=bifrost_status,
                message="Bifrost_client::error_send_to_queue",
                send_message=message,
                topic=topic,
            )
            raise ErrorSendingToBifrostClient()
