from api.domain.abstract_classes.services.funding_and_withdrawal.money_flow_resolvers.abstract_class import \
    MoneyFlowResolverAbstract
from datetime import datetime, timedelta
from api.repositories.funding_and_withdrawal.realtime.repository import RealtimeFundingAndWithdrawalRepository


class TransfersBetweenSinacorAndDriveWealth(MoneyFlowResolverAbstract):
    funding_and_withdrawal_realtime_data_repository = RealtimeFundingAndWithdrawalRepository

    async def _get_spread(self) -> float:
        cash_conversion_references = self._get_cash_conversion_references()
        spread = await self.funding_and_withdrawal_realtime_data_repository.get_tax(
            cash_conversion=cash_conversion_references)

        return spread

    async def _get_tax(self) -> float:
        cash_conversion_references = self._get_cash_conversion_references()
        tax = await self.funding_and_withdrawal_realtime_data_repository.get_tax(
            cash_conversion=cash_conversion_references)

        return tax

    async def _convert_value(self) -> float:
        cash_conversion_references = self._get_cash_conversion_references()
        conversion_base = await self.funding_and_withdrawal_realtime_data_repository.get_currency_quote(
            cash_conversion=cash_conversion_references)

        base_value = await self._get_base_value()
        spread = await self._get_spread()
        tax = await self._get_tax()

        return (base_value - ((base_value * spread) + (base_value * tax))) / conversion_base

    async def _calculate_due_date(self) -> datetime:
        return datetime.utcnow() + timedelta(days=1)

    def _get_topic_name(self) -> str:
        return "tranfers_between_sinacor_and_drive_wealth"
