from models import AddressBook
from .decorators import input_error
from .dispatcher import contact_command


@contact_command("add")
@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: add <name>"
    name = args[0]
    book.get_or_create_record(name)
    return "Contact added."


@contact_command("delete")
@input_error
def delete_contact(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: delete <name>"
    name = args[0]
    book.delete(name)
    return f"Contact '{name}' deleted."


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


# ============================================================================
# DYNAMIC COMMAND REGISTRATION
# ============================================================================

def _get_record_or_fail(book: AddressBook, name: str):
    """Helper to get a record or raise an error."""
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact '{name}' not found.")
    return record


def register_collection_commands():
    """
    Dynamically generate and register CRUD commands for all fields 
    in Record.COLLECTIONS.
    
    For each field (e.g., "phones", "emails"), generates:
    - add-{entity}: Add item to collection
    - change-{entity}: Change item in collection  
    - remove-{entity}: Remove item from collection
    - show-{entity}: Display all items in collection
    """
    from models import Record
    
    _SINGULAR = {"phones": "phone", "emails": "email", "addresses": "address"}

    for field in Record.COLLECTIONS:
        entity = _SINGULAR.get(field, field[:-1])
        
        # --- Generate ADD command ---
        def make_add(field, entity):
            @contact_command(f"add-{entity}")
            @input_error
            def add_item(args, book):
                if len(args) < 2:
                    return f"Usage: add-{entity} <name> <{entity}>"
                name = args[0]
                value = " ".join(args[1:])
                record = book.get_or_create_record(name)
                record.add(field, value)
                return f"{entity.capitalize()} added."
            return add_item
        
        # --- Generate CHANGE command ---
        def make_change(field, entity):
            @contact_command(f"change-{entity}")
            @input_error
            def change_item(args, book):
                if len(args) < 3:
                    return f"Usage: change-{entity} <name> <#> <new_{entity}>"
                name = args[0]
                record = _get_record_or_fail(book, name)
                items = getattr(record, field)
                try:
                    idx = int(args[1]) - 1
                except ValueError:
                    return f"Usage: change-{entity} <name> <#> <new_{entity}>"
                if not (0 <= idx < len(items)):
                    return f"Index out of range. Use 1-{len(items)}." if items else f"No {field} to change."
                old_value = items[idx].value
                new_value = " ".join(args[2:])
                record.change(field, old_value, new_value)
                return f"{entity.capitalize()} updated."
            return change_item
        
        # --- Generate REMOVE command ---
        def make_remove(field, entity):
            @contact_command(f"remove-{entity}")
            @input_error
            def remove_item(args, book):
                if len(args) < 2:
                    return f"Usage: remove-{entity} <name> <#>"
                name = args[0]
                record = _get_record_or_fail(book, name)
                items = getattr(record, field)
                try:
                    idx = int(args[1]) - 1
                except ValueError:
                    return f"Usage: remove-{entity} <name> <#>"
                if not (0 <= idx < len(items)):
                    return f"Index out of range. Use 1-{len(items)}." if items else f"No {field} to remove."
                old_value = items[idx].value
                record.remove(field, old_value)
                return f"{entity.capitalize()} removed."
            return remove_item
        
        # --- Generate SHOW command ---
        def make_show(field, entity):
            @contact_command(f"show-{field}")
            @input_error
            def show_items(args, book):
                if len(args) < 1:
                    return f"Usage: show-{field} <name>"
                name = args[0]
                record = _get_record_or_fail(book, name)
                items = getattr(record, field)
                if not items:
                    return f"No {field}."
                return "\n".join(f"  {i + 1}. {item.value}" for i, item in enumerate(items))
            return show_items
        
        # Register all commands for this field
        make_add(field, entity)
        make_change(field, entity)
        make_remove(field, entity)
        make_show(field, entity)


# Auto-register collection commands on module import
register_collection_commands()
