from .storage import AppContext
from .handlers import dispatch_command
from . import ui


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def main():
    ctx = AppContext.load()
    ui.print_welcome()

    while True:
        user_input = ui.ask()
        command, args = parse_input(user_input)

        if not command:
            ui.print_info("Type 'help' to see available commands.")
            continue

        if command in ("close", "exit"):
            ctx.save()
            ui.print_info("Data saved. Good bye!")
            break

        elif command == "hello":
            ui.print_result("How can I help you?")

        elif command == "help":
            ui.print_help()

        else:
            result = dispatch_command(command, args, ctx)
            ui.print_result(result)
            ctx.save()


if __name__ == "__main__":
    main()
