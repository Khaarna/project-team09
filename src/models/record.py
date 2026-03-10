from datetime import timedelta
from .fields import Name, Phone, Email, Address, Birthday


class Record:
    def __init__(self, name: Name):
        if not isinstance(name, Name):
            raise TypeError("Expected Name instance.")
        self.name = name
        self._phones: list[Phone] = []
        self._emails: list[Email] = []
        self.birthday: Birthday | None = None
        self.address: Address | None = None

    @property
    def phones(self):
        return tuple(self._phones)

    @property
    def emails(self):
        return tuple(self._emails)

    # --- Phone ---

    def find_phone(self, phone: str) -> Phone:
        for p in self._phones:
            if p.value == phone:
                return p
        raise ValueError(f"Phone not found.")

    def add_phone(self, phone: str | Phone) -> None:
        if isinstance(phone, str):
            phone = Phone(phone)
        if phone in self._phones:
            raise ValueError("Phone already exists.")
        self._phones.append(phone)

    def change_phone(self, old_phone: str, new_phone: str) -> None:
        phone_obj = self.find_phone(old_phone)
        new_phone_obj = Phone(new_phone)
        index = self._phones.index(phone_obj)
        self._phones[index] = new_phone_obj

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)
        self._phones.remove(phone_obj)

    # --- Email ---

    def find_email(self, email: str):
        pass  # TODO

    def add_email(self, email) -> None:
        pass  # TODO

    def remove_email(self, email: str) -> None:
        pass  # TODO

    # --- Birthday ---

    def add_birthday(self, birthday: str | Birthday) -> None:
        if isinstance(birthday, str):
            birthday = Birthday(birthday)
        if self.birthday is not None:
            raise ValueError("Birthday already set.")
        self.birthday = birthday

    def show_birthday(self) -> str:
        return str(self.birthday) if self.birthday else "Birthday not set."

    def get_congratulation_date(self):
        if not self.birthday:
            return None
        birthday_date = self.birthday.next_birthday()
        if birthday_date.weekday() == 5:
            birthday_date += timedelta(days=2)
        elif birthday_date.weekday() == 6:
            birthday_date += timedelta(days=1)
        return birthday_date

    # --- Address ---

    def add_address(self, address) -> None:
        pass  # TODO

    # --- Display ---

    def __str__(self):
        # TODO: format all fields (name, phones, emails, birthday, address)
        phones = ", ".join(p.value for p in self._phones) or "no phones"
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"{self.name.value}: {phones}{birthday}"