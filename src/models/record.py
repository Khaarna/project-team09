from datetime import timedelta
from .fields import Name, Phone, Email, Address, Birthday


class CRUDMixin:
    """Mixin providing generic CRUD operations for value object collections."""

    def _make_item(self, cls, value):
        item = cls(value) if not isinstance(value, cls) else value
        return item.value, item

    def _add_item(self, collection: dict, cls, value):
        key, item = self._make_item(cls, value)
        if key in collection:
            raise ValueError(f"{cls.__name__} already exists.")
        collection[key] = item
        return item

    def _find_item(self, collection: dict, cls, value):
        key = value.value if isinstance(value, cls) else cls.normalize(value)
        return collection.get(key)

    def _remove_item(self, collection: dict, cls, value):
        key = value.value if isinstance(value, cls) else cls.normalize(value)
        if key not in collection:
            raise ValueError(f"{cls.__name__} not found.")
        del collection[key]

    def _change_item(self, collection: dict, cls, old_value, new_value):
        self._remove_item(collection, cls, old_value)
        return self._add_item(collection, cls, new_value)


class Record(CRUDMixin):
    """Contact record with phones, emails, birthday, and address."""
    
    COLLECTIONS = {
        "phones": Phone,
        "emails": Email,
        "addresses": Address,
    }
    
    def __init__(self, name: Name):
        if not isinstance(name, Name):
            raise TypeError("Expected Name instance.")
        self.name = name
        for field in self.COLLECTIONS:
            setattr(self, f"_{field}", {})
        self._birthday: Birthday | None = None

    @property
    def phones(self):
        return tuple(self._phones.values())

    @property
    def emails(self):
        return tuple(self._emails.values())

    @property
    def addresses(self):
        return tuple(self._addresses.values())

    @property
    def birthday(self):
        return self._birthday

    # --- Unified CRUD Interface ---

    def _get_collection(self, field: str):
        """Get the collection for a field."""
        return getattr(self, f"_{field}")

    def _resolve(self, field: str):
        """Resolve field name to (collection, class) tuple."""
        return self._get_collection(field), self.COLLECTIONS[field]

    def add(self, field: str, value):
        """Add an item to a collection (phones, emails)."""
        collection, cls = self._resolve(field)
        return self._add_item(collection, cls, value)

    def find(self, field: str, value):
        """Find an item in a collection."""
        collection, cls = self._resolve(field)
        return self._find_item(collection, cls, value)

    def change(self, field: str, old_value, new_value):
        """Change an item in a collection."""
        collection, cls = self._resolve(field)
        return self._change_item(collection, cls, old_value, new_value)

    def remove(self, field: str, value):
        """Remove an item from a collection."""
        collection, cls = self._resolve(field)
        self._remove_item(collection, cls, value)

    # --- Birthday ---

    def _set_birthday(self, birthday: Birthday | None, *, allow_override: bool = False):
        """Set birthday with optional override control."""
        if birthday is not None and not isinstance(birthday, Birthday):
            raise TypeError("Expected Birthday instance")

        if birthday is not None and self._birthday is not None and not allow_override:
            raise ValueError("Birthday already exists. Use change_birthday to update.")

        self._birthday = birthday

    def add_birthday(self, birthday: str | Birthday) -> None:
        """Add birthday. Raises if already set."""
        if isinstance(birthday, str):
            birthday = Birthday(birthday)
        self._set_birthday(birthday)

    def change_birthday(self, birthday: str | Birthday) -> None:
        """Change an existing birthday."""
        if isinstance(birthday, str):
            birthday = Birthday(birthday)
        self._set_birthday(birthday, allow_override=True)

    def remove_birthday(self) -> None:
        """Remove the birthday."""
        self._set_birthday(None, allow_override=True)

    def show_birthday(self) -> str:
        """Return birthday as string, or 'Birthday not set.'"""
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

    # --- Display ---

    def __str__(self):
        """Format record as string with all fields."""
        parts = [self.name.value]

        # Add collection fields dynamically
        for field in self.COLLECTIONS:
            collection = getattr(self, f"_{field}")
            if collection:
                items = ", ".join(item.value for item in collection.values())
                parts.append(f"{field.capitalize()}: {items}")

        # Add birthday if set
        if self.birthday:
            parts.append(f"Birthday: {self.birthday}")

        return "; ".join(parts)