CONTACT_COMMANDS: dict = {}
NOTE_COMMANDS: dict = {}


def contact_command(name: str):
    def decorator(func):
        if name in CONTACT_COMMANDS:
            raise ValueError(f"Contact command '{name}' already registered")
        CONTACT_COMMANDS[name] = func
        return func
    return decorator


def note_command(name: str):
    def decorator(func):
        if name in NOTE_COMMANDS:
            raise ValueError(f"Note command '{name}' already registered")
        NOTE_COMMANDS[name] = func
        return func
    return decorator


def dispatch_command(command: str, args: list[str], ctx) -> str:
    if command in CONTACT_COMMANDS:
        return CONTACT_COMMANDS[command](args, ctx.book)
    if command in NOTE_COMMANDS:
        return NOTE_COMMANDS[command](args, ctx.notes)
    return f"Unknown command '{command}'. Type 'help' to see available commands."
