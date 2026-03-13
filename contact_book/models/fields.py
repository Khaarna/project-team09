import re
from datetime import datetime, date


class Field:
    def __init__(self, value):
        if value is None:
            raise ValueError("Value cannot be None")
        self._value = self.validate(value)

    def validate(self, value):
        return value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)

    @classmethod
    def normalize(cls, value: str) -> str:
        """Normalize raw input to canonical key form, without validation."""
        return value.strip()


class Name(Field):
    def validate(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        return value.strip()


class Phone(Field):
    @classmethod
    def normalize(cls, value: str) -> str:
        value = value.strip()
        if value.startswith("+"):
            value = value[1:]
        return value

    def validate(self, value):
        value = self.normalize(value)
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")
        return value

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value!r})"


class Email(Field):
    _PATTERN = re.compile(r"^[^@\s]+@([\w-]+\.)+[A-Za-z]{2,}$")

    def validate(self, value):
        value = self.normalize(value)
        if not self._PATTERN.fullmatch(value):
            raise ValueError("Invalid email format. Expected: user@example.com")
        return value


class Address(Field):
    def validate(self, value):
        value = self.normalize(value)
        if not (5 <= len(value) <= 200):
            raise ValueError("Address must be between 5 and 200 characters.")
        return value


class Tag(Field):
    @classmethod
    def normalize(cls, value: str) -> str:
        return value.strip().lower()

    def validate(self, value):
        value = self.normalize(value)
        if not value:
            raise ValueError("Tag cannot be empty.")
        if not re.match(r'^[a-z0-9_-]+$', value):
            raise ValueError("Tag can only contain letters, digits, hyphens and underscores.")
        return value


class Birthday(Field):
    def validate(self, value):
        value = value.strip()
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")

    def next_birthday(self) -> date:
        today = date.today()
        try:
            next_bd = self.value.replace(year=today.year)
        except ValueError:
            next_bd = date(today.year, 3, 1)  # Feb 29 → Mar 1

        if next_bd < today:
            try:
                next_bd = next_bd.replace(year=today.year + 1)
            except ValueError:
                next_bd = date(today.year + 1, 3, 1)

        return next_bd

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
