from dataclasses import dataclass


# TODO: Verificar se ainda deve existir model de balanco

@dataclass(init=True)
class Balance:
    value: float

    def __repr__(self):
        balance = {
            "value": self.value,
        }

        return balance
