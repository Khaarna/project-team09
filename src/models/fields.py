import re
from datetime import datetime, date


class Field:
    def __init__(self, value):
        if value is None:
            raise ValueError("Value cannot be None.")
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


class Name(Field):
    def validate(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        return value.strip()


class Phone(Field):
    def validate(self, value):
        value = value.strip()
        
        if value.startswith("+"):
            value = value[1:]
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain exactly 10 digits.")
        return value

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value!r})"


class Email(Field):

    EMAIL_PATTERN = re.compile(r"^[^@\s]+@([\w-]+\.)+[A-Za-z]{2,}$")

    def validate(self, value):
        value = value.strip()
    
        if not self.EMAIL_PATTERN.fullmatch(value):
            raise ValueError("Invalid email format")

        return value
        

class Address(Field):
    def validate(self, value):
        value = value.strip()

        if not value:
            raise ValueError("Address cannot be empty.")

        return value


class Tag(Field):
    def validate(self, value):
        # TODO
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
