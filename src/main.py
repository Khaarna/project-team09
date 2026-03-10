from storage import save_data, load_data
from handlers import (
    add_contact, change_phone, delete_contact,
    show_phone, show_contact, show_all, search_contacts,
    add_email, add_address,
    add_birthday, show_birthday, birthdays,
    add_note, show_note, edit_note, delete_note,
    show_all_notes, search_notes,
    add_tag, remove_tag, search_by_tag,
)

HELP_TEXT = """
Available commands:

  CONTACTS
  --------
  add [name] [phone]               Add contact or new phone to existing contact
  change [name] [old] [new]        Change phone number
  delete [name]                    Delete contact
  phone [name]                     Show contact's phones
  info [name]                      Show full contact info
  all                              Show all contacts
  search [query]                   Search contacts by name, phone or email
  add-email [name] [email]         Add email to contact
  add-address [name] [address...]  Add address to contact
  add-birthday [name] [DD.MM.YYYY] Add birthday
  show-birthday [name]             Show birthday
  birthdays [days]                 Show upcoming birthdays (default: 7 days)

  NOTES
  -----
  add-note [title] [content...]    Add new note
  note [title]                     Show note
  edit-note [title] [content...]   Edit note content
  delete-note [title]              Delete note
  notes                            Show all notes
  search-notes [query]             Search notes by title or content
  add-tag [title] [tag]            Add tag to note
  remove-tag [title] [tag]         Remove tag from note
  search-tag [tag]                 Search notes by tag

  OTHER
  -----
  hello                            Greeting
  help                             Show this help
  close / exit                     Save and exit
"""


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def main():
    book, notes = load_data()
    print("Welcome to Contact Book Assistant!")
    print("Type 'help' to see available commands.")

    commands = {
        # Contacts
        "add":           lambda args: add_contact(args, book),
        "change":        lambda args: change_phone(args, book),
        "delete":        lambda args: delete_contact(args, book),
        "phone":         lambda args: show_phone(args, book),
        "info":          lambda args: show_contact(args, book),
        "all":           lambda args: show_all(book),
        "search":        lambda args: search_contacts(args, book),
        "add-email":     lambda args: add_email(args, book),
        "add-address":   lambda args: add_address(args, book),
        "add-birthday":  lambda args: add_birthday(args, book),
        "show-birthday": lambda args: show_birthday(args, book),
        "birthdays":     lambda args: birthdays(args, book),
        # Notes
        "add-note":      lambda args: add_note(args, notes),
        "note":          lambda args: show_note(args, notes),
        "edit-note":     lambda args: edit_note(args, notes),
        "delete-note":   lambda args: delete_note(args, notes),
        "notes":         lambda args: show_all_notes(notes),
        "search-notes":  lambda args: search_notes(args, notes),
        "add-tag":       lambda args: add_tag(args, notes),
        "remove-tag":    lambda args: remove_tag(args, notes),
        "search-tag":    lambda args: search_by_tag(args, notes),
    }

    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)

        if not command:
            continue

        if command in ("close", "exit"):
            save_data(book, notes)
            print("Data saved. Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help":
            print(HELP_TEXT)

        elif command in commands:
            print(commands[command](args))

        else:
            print(f"Unknown command '{command}'. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
