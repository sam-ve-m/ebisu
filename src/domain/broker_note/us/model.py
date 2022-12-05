from dataclasses import dataclass


@dataclass
class Confirmation:
    description: str
    file_key: str

    def to_dict(self):
        confirmation_dict = {"description": self.description, "file_key": self.file_key}
        return confirmation_dict


@dataclass
class Statement:
    broker_note_link: str

    def to_dict(self):
        statement_dict = {
            "broker_note_link": self.broker_note_link,
        }
        return statement_dict
