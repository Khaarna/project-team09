from storage import save_data, load_data
from handlers import dispatch_command

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
  search [keyword]                 Search contacts by name, phone or email
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


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def main():
    book, notes = load_data()
    print("Welcome to Contact Book Assistant!")
    print("Type 'help' to see available commands.")

    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)

        if not command:
            print("Please type a command or 'help' to see available commands.")
            continue

        if command in ("close", "exit"):
            save_data(book, notes)
            print("Data saved. Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help":
            print(HELP_TEXT)

        else:
            print(dispatch_command(command, args, book, notes))


if __name__ == "__main__":
    main()
