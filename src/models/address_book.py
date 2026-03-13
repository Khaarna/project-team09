from datetime import date
from .record import Record
from .fields import Name


class AddressBook:
    def __init__(self):
        self._records: dict[str, Record] = {}

    @property
    def records(self):
        return tuple(self._records.values())

    def get_or_create_record(self, name: str) -> Record:
        key = name.lower()
        record = self._records.get(key)
        if record is None:
            record = Record(Name(name))
            self._records[key] = record
        return record

    def find(self, name: str) -> Record | None:
        return self._records.get(name.lower())

    def delete(self, name: str) -> None:
        key = name.lower()
        if key not in self._records:
            raise KeyError(f"Contact '{name}' not found.")
        del self._records[key]

    def search(self, query: str) -> list[Record]:
        term = query.strip().lower()
        if not term:
            return list(self._records.values())
        return [
            record for record in self._records.values()
            if term in record.name.value.lower()
            or any(term in p.value for p in record.phones)
            or any(term in e.value.lower() for e in record.emails)
            or any(term in a.value.lower() for a in record.addresses)
        ]

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = date.today()
        upcoming = []
        for record in self._records.values():
            congratulation_date = record.get_congratulation_date()
            if congratulation_date is None:
                continue
            delta_days = (congratulation_date - today).days
            if 0 <= delta_days <= days:
                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })
        return upcoming

    def __iter__(self):
        return iter(self._records.values())

    def __str__(self):
        return "\n".join(str(record) for record in self)
