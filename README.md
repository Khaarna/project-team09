# Contact Book Assistant

A CLI application for managing contacts and notes, built with Python.

## Features

- **Contacts** — store names, phone numbers, emails, addresses and birthdays
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
| `add <name> <phone>` | Add contact or new phone to existing contact |
| `change <name> <old> <new>` | Change phone number |
| `delete <name>` | Delete contact |
| `phone <name>` | Show contact's phones |
| `info <name>` | Show full contact info |
| `all` | Show all contacts |
| `search <keyword>` | Search contacts by name, phone or email |
| `add-email <name> <email>` | Add email to contact |
| `add-address <name> <address...>` | Add address to contact (multi-word supported) |
| `add-birthday <name> <DD.MM.YYYY>` | Add birthday |
| `show-birthday <name>` | Show birthday |
| `birthdays [days]` | Show upcoming birthdays (default: 7 days) |

### Notes

| Command | Description |
|---|---|
| `add-note <title> [content...]` | Add new note (multi-word content supported) |
| `note <title>` | Show note |
| `edit-note <title> <content...>` | Edit note content (multi-word supported) |
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

- **Names and titles** are single words (spaces are not supported)
- **Tags** can only contain letters, digits, hyphens (`-`) and underscores (`_`); automatically lowercased
- **Phone numbers** must be exactly 10 digits (leading `+` is accepted and stripped)
- **Birthdays** must be in `DD.MM.YYYY` format

## Project Structure

```
src/
├── main.py               # Entry point, CLI loop
├── storage.py            # Save/load with integrity check
├── models/
│   ├── fields.py         # Field, Name, Phone, Email, Address, Tag, Birthday
│   ├── record.py         # Contact record
│   ├── address_book.py   # AddressBook collection
│   ├── note.py           # Note entity
│   └── notes_book.py     # NotesBook collection
└── handlers/
    ├── dispatcher.py     # Command registration and dispatch
    ├── decorators.py     # @input_error decorator
    ├── contact_handlers.py
    └── note_handlers.py
```

## Data

Contact and notes data is stored in `data/` at the project root (git-ignored). The folder is created automatically on first save.

