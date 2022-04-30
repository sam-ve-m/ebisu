from api.domain.enums.currency import Currency
from api.domain.enums.region import Region


country_to_currency = {
    Region.BR: Currency.BRL,
    Region.US: Currency.USD
}