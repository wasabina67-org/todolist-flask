from dataclasses import dataclass


@dataclass
class TodoValidator:
    name: str

    def __post_init__(self):
        self.validate_name()

    def validate_name(self):
        if not self.name:
            raise ValueError("Todo must be a non-empty string.")
        if len(self.name) > 80:
            raise ValueError("Todo must not be longer than 80 characters.")
