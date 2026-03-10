from .fields import Name, Phone, Email, Birthday, Address


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.address = None

    # --- Phone ---

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        p = self.find_phone(phone)
        if p:
            self.phones.remove(p)
        else:
            raise ValueError(f"Phone '{phone}' not found")

    def edit_phone(self, old_phone, new_phone):
        p = self.find_phone(old_phone)
        if p:
            p.value = new_phone
        else:
            raise ValueError(f"Phone '{old_phone}' not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # --- Email ---

    def add_email(self, email):
        pass

    def remove_email(self, email):
        pass

    def find_email(self, email):
        pass

    # --- Birthday ---

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # --- Address ---

    def add_address(self, address):
        pass

    # --- Display ---

    def __str__(self):
        pass
