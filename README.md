# Contact Book Assistant

A CLI application for managing contacts and notes, built with Python and [rich](https://github.com/Textualize/rich).

## Features

- **Contacts** — store names, multiple phones, emails, addresses and a birthday per contact
- **Notes** — create and manage text notes with tags
- **Upcoming birthdays** — list contacts with birthdays in the next N days
- **Persistent storage** — data is saved automatically after every command with SHA-256 integrity check
- **Rich terminal UI** — tables, panels and colour-coded output via the `rich` library
- **Tab completion** — command names and contact/note names complete on TAB via `prompt_toolkit`

## Requirements

- Python 3.10+
- Dependencies: `rich>=13.0`, `prompt_toolkit>=3.0` (installed automatically)

## Installation

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

Install the package:

```bash
pip install .
```

This installs all dependencies (`rich`, `prompt_toolkit`) and registers the `contact-book` command.

## Running

After installation:

```bash
contact-book
```

Or without installing, from the project root:

```bash
python -m contact_book
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
| `add-address <name> <address>` | Add address to contact (multi-word supported) |
| `change-address <name> <#> <address>` | Change address by index |
| `remove-address <name> <#>` | Remove address by index |
| `show-addresses <name>` | Show all addresses (numbered) |

### Birthday

| Command | Description |
|---|---|
| `add-birthday <name> <DD.MM.YYYY>` | Add birthday |
| `change-birthday <name> <DD.MM.YYYY>` | Change birthday |
| `remove-birthday <name>` | Remove birthday |
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
| `sort-by-tag` | Show all notes sorted by tag |

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

### CRUDMixin (`record.py`)

Generic dict-based CRUD operations defined in `record.py` and inherited by `Record` for all multi-value collections. Uses the field's `.value` as the dict key, giving O(1) lookups and automatic duplicate prevention. Each `Field` subclass provides a `normalize()` classmethod used to canonicalize keys before lookup.

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

### UI (`ui.py`)

All terminal output goes through `ui.py`, which uses `rich` for visual rendering:

- Contacts are displayed in a **Table** (for `all`/`search`) or a **Panel** (for `info`)
- Notes are displayed as individual **Panels** with `#tag` highlighting
- Success messages are green, errors are bold red, usage hints are yellow
- The `help` command renders a structured table grouped by section

Handlers call `ui.show_contact()` / `ui.show_notes()` etc. directly and return `None`; plain-string-returning handlers are rendered by `ui.print_result()` from the main loop.

### Tab Completion (`completion.py`)

`ContactBookCompleter` (a `prompt_toolkit.Completer`) provides context-aware TAB completion:

- **Word 1** — completes all registered command names (built once, cached)
- **Word 2** — completes contact names for commands like `info`, `delete`, `add-phone`, etc., or note titles for `note`, `edit-note`, `add-tag`, etc.

The completer holds a live reference to `AppContext`, so newly added contacts and notes are immediately available as completions without any cache invalidation.

### Command Dispatcher (`dispatcher.py`)

Two independent registries (`CONTACT_COMMANDS`, `NOTE_COMMANDS`) populated by `@contact_command` / `@note_command` decorators. `dispatch_command()` checks both and returns a standard error message for unknown commands.

### AppContext and Storage (`storage.py`)

`AppContext` owns the application state (`book`, `notes`) and encapsulates all persistence logic:

```python
ctx = AppContext.load()   # deserialize from disk, verify SHA-256 hash
ctx.save()                # atomic write (tmp + os.replace) + update hash
```

Data is pickled to `data/` with a SHA-256 hash stored alongside. On load the hash is verified; a mismatch discards the file and starts fresh. Saves happen after every command, so a crash never loses more than one operation.

## Project Structure

```
contact_book/
├── __init__.py
├── __main__.py           # Entry point (python -m contact_book / contact-book)
├── storage.py            # AppContext: pickle persistence + SHA-256 integrity
├── ui.py                 # Rich-based terminal rendering
├── completion.py         # TAB completion via prompt_toolkit
├── models/
│   ├── fields.py         # Value objects (Field subclasses)
│   ├── record.py         # CRUDMixin + Record aggregate root
│   ├── address_book.py   # AddressBook collection + search
│   ├── note.py           # Note entity
│   └── notes_book.py     # NotesBook collection + sort_by_tag
└── handlers/
    ├── dispatcher.py     # Command registries and dispatch
    ├── decorators.py     # @input_error decorator
    ├── contact_handlers.py  # Contact commands + dynamic registration
    └── note_handlers.py     # Note commands
```

## Testing

All tests live in a single file, `tests.py`, at the project root:

```bash
python tests.py
```

No extra dependencies required — the test runner is built-in. Each test group prints its individual checks and the run exits with code `0` on success or `1` on failure.

## Data

Contact and notes data is stored in `data/` at the project root (git-ignored). The folder is created automatically on first save.

