from dataclasses import dataclass


@dataclass(init=True)
class Balance:
    value: float

    def __repr__(self):
        balance = {
            "value": self.value,
        }

        return balance

