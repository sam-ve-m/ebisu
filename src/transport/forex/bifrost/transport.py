# Ebisu
from src.domain.enums.forex.operations import OperationType
from src.domain.exceptions.transport.forex.exception import ErrorSendingToBifrostClient
from src.domain.models.forex.proposal.execution_request_data.model import ExecutionModel

# Third party
from bifrost_client import BifrostClient, BifrostTopics
from etria_logger import Gladsheim


class BifrostTransport:
    ted_topic = BifrostTopics.TRANSFERS_BETWEEN_SINACOR_AND_FOREX_EXCHANGE
    buy_power_topic = BifrostTopics.ADD_DRIVE_WEALTH_BUY_POWER
    withdraw_topic = BifrostTopics.DRIVE_WEALTH_WITHDRAW

    @classmethod
    async def send_solicitation_to_queue(cls, execution_model: ExecutionModel) -> True:
        message = execution_model.get_bifrost_template()
        if execution_model.operation_type == OperationType.BRL_TO_USD:
            await cls.send_to_bifrost(message=message, topic=cls.ted_topic)
            await cls.send_to_bifrost(message=message, topic=cls.buy_power_topic)
            return True
        await cls.send_to_bifrost(message=message, topic=cls.withdraw_topic)
        return True

    @staticmethod
    async def send_to_bifrost(message: dict, topic: BifrostTopics):
        success, bifrost_status = await BifrostClient.send_to_bifrost(
            message=message,
            topic=topic,
        )
        if not success:
            msg = f"Bifrost_client::error_send_to_queue::{topic=}::{message=}"
            Gladsheim.error(
                bifrost_status=bifrost_status,
                message=msg
            )
            raise ErrorSendingToBifrostClient(msg=msg)
