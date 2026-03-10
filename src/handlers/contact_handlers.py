from models import AddressBook, Record
from .decorators import input_error


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args[0], args[1]
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found")
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def delete_contact(args, book: AddressBook):
    pass


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found")
    if not record.phones:
        return f"'{name}' has no phones."
    return f"{name}: {', '.join(p.value for p in record.phones)}"


@input_error
def show_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found")
    return str(record)


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    separator = "\n" + "-" * 30 + "\n"
    return separator.join(str(r) for r in book.data.values())


@input_error
def search_contacts(args, book: AddressBook):
    pass


@input_error
def add_email(args, book: AddressBook):
    pass


@input_error
def add_address(args, book: AddressBook):
    pass


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact '{name}' not found")
    if record.birthday is None:
        return f"'{name}' has no birthday set."
    return f"{name}'s birthday: {record.birthday.value}"


@input_error
def birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    if days < 0:
        raise ValueError("Number of days must be non-negative")
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No upcoming birthdays in the next {days} days."
    lines = [f"Upcoming birthdays (next {days} days):"]
    for item in upcoming:
        lines.append(f"  {item['name']}: {item['congratulation_date']}")
    return "\n".join(lines)
