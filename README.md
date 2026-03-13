# Contact Book Assistant

A CLI application for managing contacts and notes, built with Python.

## Features

- **Contacts** — store names, multiple phones, emails, addresses and a birthday per contact
- **Notes** — create and manage text notes with tags
- **Upcoming birthdays** — list contacts with birthdays in the next N days
- **Persistent storage** — data is saved automatically on exit with SHA-256 integrity check

## Requirements

- Python 3.10+

## Running

```bash
cd src
py main.py
```

## Commands

### Contacts

| Command | Description |
|---|---|
| `add <name>` | Add a new contact |
| `delete <name>` | Delete contact |
| `info <name>` | Show full contact info |
| `all` | Show all contacts |
| `search <keyword>` | Search by name, phone, email or address |

### Phones

| Command | Description |
|---|---|
| `add-phone <name> <phone>` | Add phone to contact |
| `change-phone <name> <#> <new>` | Change phone by index |
| `remove-phone <name> <#>` | Remove phone by index |
| `show-phones <name>` | Show all phones (numbered) |

### Emails

| Command | Description |
|---|---|
| `add-email <name> <email>` | Add email to contact |
| `change-email <name> <#> <new>` | Change email by index |
| `remove-email <name> <#>` | Remove email by index |
| `show-emails <name>` | Show all emails (numbered) |

### Addresses

| Command | Description |
|---|---|
| `add-address <name> <addr...>` | Add address to contact (multi-word supported) |
| `change-address <name> <#> <addr...>` | Change address by index |
| `remove-address <name> <#>` | Remove address by index |
| `show-addresses <name>` | Show all addresses (numbered) |

### Birthday

| Command | Description |
|---|---|
| `add-birthday <name> <DD.MM.YYYY>` | Add birthday |
| `show-birthday <name>` | Show birthday |
| `birthdays [days]` | Show upcoming birthdays (default: 7 days) |

### Notes

| Command | Description |
|---|---|
| `add-note <title> [content...]` | Add new note |
| `note <title>` | Show note |
| `edit-note <title> <content...>` | Edit note content |
| `delete-note <title>` | Delete note |
| `notes` | Show all notes |
| `search-notes <keyword...>` | Search notes by title or content |
| `add-tag <title> <tag>` | Add tag to note |
| `remove-tag <title> <tag>` | Remove tag from note |
| `search-tag <tag>` | Search notes by tag |

### Other

| Command | Description |
|---|---|
| `hello` | Greeting |
| `help` | Show available commands |
| `close` / `exit` | Save data and exit |

## Input Rules

- **Names and titles** are single words (spaces not supported)
- **Phone numbers** must be exactly 10 digits (leading `+` is accepted and stripped)
- **Emails** must match `user@example.com` format
- **Addresses** must be between 5 and 200 characters; multi-word supported
- **Birthdays** must be in `DD.MM.YYYY` format
- **Tags** can only contain letters, digits, hyphens (`-`) and underscores (`_`); automatically lowercased
- **Indexes** (`#`) are 1-based; use `show-phones` / `show-emails` / `show-addresses` to see them

## Architecture

### Value Objects (`fields.py`)

Each field type is a `Field` subclass that validates input on construction and is immutable after creation. This makes invalid state unrepresentable — a `Phone("abc")` raises immediately rather than failing later.

```
Field
├── Name       — non-empty string
├── Phone      — exactly 10 digits, strips leading +
├── Email      — validated against regex pattern
├── Address    — 5–200 characters
├── Tag        — lowercase alphanumeric with - and _
└── Birthday   — DD.MM.YYYY → date, with next_birthday() leap-year handling
```

### CRUDMixin (`fields.py`)

Generic dict-based CRUD operations used by `Record` for all multi-value collections. Uses the field's `.value` as the dict key, giving O(1) lookups and automatic duplicate prevention.

```python
class CRUDMixin:
    def _add_item(collection, cls, value): ...
    def _find_item(collection, cls, value): ...
    def _remove_item(collection, cls, value): ...
    def _change_item(collection, cls, old, new): ...
```

### Record (`record.py`)

`Record` inherits `CRUDMixin` and declares which fields are multi-value collections via a class-level registry:

```python
class Record(CRUDMixin):
    COLLECTIONS = {
        "phones":    Phone,
        "emails":    Email,
        "addresses": Address,
    }
```

A unified interface delegates to the mixin:

```python
record.add("phones", "1234567890")
record.change("emails", old, new)
record.remove("addresses", old)
```

`Birthday` is a single-value field with its own `add_birthday` / `change_birthday` / `remove_birthday` methods that enforce the 0-or-1 cardinality explicitly.

### Dynamic Command Registration (`contact_handlers.py`)

Rather than writing handlers for each field by hand, `register_collection_commands()` reads `Record.COLLECTIONS` at import time and auto-generates four commands per field: `add-{entity}`, `change-{entity}`, `remove-{entity}`, `show-{field}`. Adding a new collection field to `Record.COLLECTIONS` automatically produces its full set of CLI commands.

Change and remove commands accept a **1-based index** instead of requiring the user to retype the existing value. The handler resolves the index to the actual stored value before calling the model.

### Command Dispatcher (`dispatcher.py`)

Two independent registries (`CONTACT_COMMANDS`, `NOTE_COMMANDS`) populated by `@contact_command` / `@note_command` decorators. `dispatch_command()` checks both and returns a standard error message for unknown commands.

### Storage (`storage.py`)

Data is pickled to `data/` with a SHA-256 hash stored alongside. On load the hash is verified; a mismatch raises rather than silently loading corrupt data.

## Project Structure

```
src/
├── main.py               # Entry point, CLI loop, help text
├── storage.py            # Pickle save/load with SHA-256 integrity check
├── models/
│   ├── fields.py         # Value objects + CRUDMixin
│   ├── record.py         # Contact aggregate root (uses CRUDMixin)
│   ├── address_book.py   # AddressBook collection + search
│   ├── note.py           # Note entity
│   └── notes_book.py     # NotesBook collection
└── handlers/
    ├── dispatcher.py     # Command registries and dispatch
    ├── decorators.py     # @input_error decorator
    ├── contact_handlers.py  # Contact commands + dynamic registration
    └── note_handlers.py     # Note commands
```

## Data

Contact and notes data is stored in `data/` at the project root (git-ignored). The folder is created automatically on first save.

