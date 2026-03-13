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
        return "Usage: search <query>"
    pass  # TODO


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


    ##################################################################
    #Команда show_all як ГЕНЕРАТОР: архітектура query-pipeline  
    # економія пам'яті, можлива фільтрація, пагінація, сортування.
    # Для кожного фільтра може бути своя команда:
    # show-all-contacts, show-by-tag <tag>, show-upcoming <days>

# Pipeline Layer for show-all command - mini-query engine

from itertools import islice
from datetime import date, timedelta

def contacts(book):
    yield from book

#filters:

FILTERS = {
    "name": filter_name,
    "tag": filter_tag,
    "upcoming": filter_upcoming,
}

def filter_field(records, field, text):
    text = text.lower()

    for r in records:

        items = getattr(r, f"_{field}", None)

        if not items:
            continue

        if any(text in i.value.lower() for i in items.values()):
            yield r

def format_contacts(records):

    for r in records:

        parts = [r.name.value]

        parts.extend(
            f"{field}: {', '.join(i.value for i in getattr(r, f'_{field}').values())}"
            for field in Record.COLLECTIONS
            if getattr(r, f"_{field}")
        )

        if r.birthday:
            parts.append(f"Birthday: {r.birthday}")

        yield "; ".join(parts)

def paginate(lines, size=5):

    it = iter(lines)

    while page := list(islice(it, size)):
        yield "\n".join(page)

def query_contacts(book, filters=None, page=5):
    records = contacts(book)

    if filters:

        for func, value in filters:

            if isinstance(value, tuple):
                records = func(records, *value)
            else:
                records = func(records, value)

    lines = format_contacts(records)

    return "\n\n".join(paginate(lines, page))
    
# Commands    
from queries import (
    query_contacts,
    filter_name,
    filter_tag,
    filter_upcoming,
)


FILTERS = {
    "name": filter_name,
    "tag": filter_tag,
    "upcoming": filter_upcoming,
}

@command("show-all-contacts")
@input_error
def show_all(args, book):

    filters = []

    for arg in args:

        if "=" not in arg:
            continue

        key, value = arg.split("=", 1)
        func = FILTERS.get(key)

        if func:
            filters.append((func, value))

    return query_contacts(book, filters)
