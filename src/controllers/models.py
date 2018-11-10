from dataclasses import dataclass


@dataclass
class NewUser:
    name: str = None
    email: str = None
    type: str = None

    @property
    def as_dict(self):
        return vars(self)
