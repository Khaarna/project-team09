from storage import AppContext
from handlers import dispatch_command

HELP_TEXT = """
Available commands:

  CONTACTS
  --------
  add [name]                          Add a new contact
  delete [name]                       Delete contact
  info [name]                         Show full contact info
  all                                 Show all contacts
  search [keyword]                    Search by name, phone, email or address

  PHONES
  ------
  add-phone [name] [phone]            Add phone to contact
  change-phone [name] [#] [new]       Change phone by index
  remove-phone [name] [#]             Remove phone by index
  show-phones [name]                  Show all phones (numbered)

  EMAILS
  ------
  add-email [name] [email]            Add email to contact
  change-email [name] [#] [new]       Change email by index
  remove-email [name] [#]             Remove email by index
  show-emails [name]                  Show all emails (numbered)

  ADDRESSES
  ---------
  add-address [name] [address]        Add address to contact
  change-address [name] [#] [address] Change address by index
  remove-address [name] [#]           Remove address by index
  show-addresses [name]               Show all addresses (numbered)

  BIRTHDAY
  --------
  add-birthday [name] [DD.MM.YYYY]    Add birthday
  change-birthday [name] [DD.MM.YYYY] Change birthday
  remove-birthday [name]              Remove birthday
  show-birthday [name]                Show birthday
  birthdays [days]                    Upcoming birthdays (default: 7 days)

  NOTES
  -----
  add-note [title] [content...]       Add new note
  note [title]                        Show note
  edit-note [title] [content...]      Edit note content
  delete-note [title]                 Delete note
  notes                               Show all notes
  search-notes [query]                Search notes by title or content
  add-tag [title] [tag]               Add tag to note
  remove-tag [title] [tag]            Remove tag from note
  search-tag [tag]                    Search notes by tag
  sort-by-tag                         Show all notes sorted by tag

  OTHER
  -----
  hello                               Greeting
  help                                Show this help
  close / exit                        Save and exit
"""


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def main():
    ctx = AppContext.load()
    print("Welcome to Contact Book Assistant!")
    print("Type 'help' to see available commands.")

    while True:
        user_input = input("\nEnter a command: ")
        command, args = parse_input(user_input)

        if not command:
            print("Please type a command or 'help' to see available commands.")
            continue

        if command in ("close", "exit"):
            ctx.save()
            print("Data saved. Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help":
            print(HELP_TEXT)

        else:
            print(dispatch_command(command, args, ctx))
            ctx.save()


if __name__ == "__main__":
    main()
