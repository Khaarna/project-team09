from models import AddressBook
from .decorators import input_error
from .dispatcher import contact_command


@contact_command("add")
@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add <name> <phone>"
    name, phone = args[0], args[1]
    record = book.get_or_create_record(name)
    record.add_phone(phone)
    return "Contact updated."


@contact_command("change")
@input_error
def change_phone(args, book: AddressBook):
    if len(args) < 3:
        return "Usage: change <name> <old_phone> <new_phone>"
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found.")
    record.change_phone(old_phone, new_phone)
    return "Phone updated."


@contact_command("delete")
@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: delete <name>"
    name = args[0]
    book.delete(name)
    return f"Contact '{name}' deleted."


@contact_command("phone")
@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: phone <name>"
    name = args[0]
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found.")
    if not record.phones:
        return f"'{name}' has no phones."
    return f"{name}: {', '.join(p.value for p in record.phones)}"


@contact_command("info")
@input_error
def show_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: info <name>"
    name = args[0]
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found.")
    return str(record)


@contact_command("all")
@input_error
def show_all(args, book: AddressBook):
    return str(book) if book._records else "No contacts found."


@contact_command("search")
@input_error
def search_contacts(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: search <keyword>"
    results = book.search(args[0])
    if not results:
        return "No contacts found."
    return "\n".join(str(r) for r in results)


@contact_command("add-email")
@input_error
def add_email(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add-email <name> <email>"
    pass  # TODO


@contact_command("add-address")
@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add-address <name> <address>"
    pass  # TODO


@contact_command("add-birthday")
@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add-birthday <name> <DD.MM.YYYY>"
    name, birthday = args[0], args[1]
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found.")
    record.add_birthday(birthday)
    return "Birthday added."


@contact_command("show-birthday")
@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: show-birthday <name>"
    name = args[0]
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found.")
    return record.show_birthday()


@contact_command("birthdays")
@input_error
def birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    if days < 0:
        raise ValueError("Number of days must be non-negative.")
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No upcoming birthdays in the next {days} days."
    lines = [f"Upcoming birthdays (next {days} days):"]
    for item in upcoming:
        lines.append(f"  {item['name']}: {item['congratulation_date']}")
    return "\n".join(lines)
