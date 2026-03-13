"""
Rich-based UI rendering for the Contact Book Assistant.

All console output goes through this module so that main.py and handlers
remain decoupled from presentation concerns.  Handlers continue to return
plain strings (good for testing); this module handles the visual layer.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markup import escape
from rich import box as rich_box

console = Console()

# ---------------------------------------------------------------------------
# Startup / Help
# ---------------------------------------------------------------------------

def print_welcome() -> None:
    console.print(
        Panel.fit(
            "[bold cyan]Contact Book Assistant[/bold cyan]\n"
            "[dim]Type [bold white]help[/bold white] to see available commands.[/dim]",
            border_style="cyan",
            padding=(1, 4),
        )
    )


def print_help() -> None:
    SECTIONS = {
        "CONTACTS": [
            ("add [name]",                          "Add a new contact"),
            ("delete [name]",                       "Delete contact"),
            ("info [name]",                         "Show full contact info"),
            ("all",                                 "Show all contacts"),
            ("search [keyword]",                    "Search by name, phone, email or address"),
        ],
        "PHONES": [
            ("add-phone [name] [phone]",            "Add phone to contact"),
            ("change-phone [name] [#] [new]",       "Change phone by index"),
            ("remove-phone [name] [#]",             "Remove phone by index"),
            ("show-phones [name]",                  "Show all phones (numbered)"),
        ],
        "EMAILS": [
            ("add-email [name] [email]",            "Add email to contact"),
            ("change-email [name] [#] [new]",       "Change email by index"),
            ("remove-email [name] [#]",             "Remove email by index"),
            ("show-emails [name]",                  "Show all emails (numbered)"),
        ],
        "ADDRESSES": [
            ("add-address [name] [address]",        "Add address to contact"),
            ("change-address [name] [#] [address]", "Change address by index"),
            ("remove-address [name] [#]",           "Remove address by index"),
            ("show-addresses [name]",               "Show all addresses (numbered)"),
        ],
        "BIRTHDAY": [
            ("add-birthday [name] [DD.MM.YYYY]",    "Add birthday"),
            ("change-birthday [name] [DD.MM.YYYY]", "Change birthday"),
            ("remove-birthday [name]",              "Remove birthday"),
            ("show-birthday [name]",                "Show birthday"),
            ("birthdays [days]",                    "Upcoming birthdays (default: 7 days)"),
        ],
        "NOTES": [
            ("add-note [title] [content...]",       "Add new note"),
            ("note [title]",                        "Show note"),
            ("edit-note [title] [content...]",      "Edit note content"),
            ("delete-note [title]",                 "Delete note"),
            ("notes",                               "Show all notes"),
            ("search-notes [query]",                "Search notes by title or content"),
            ("add-tag [title] [tag]",               "Add tag to note"),
            ("remove-tag [title] [tag]",            "Remove tag from note"),
            ("search-tag [tag]",                    "Search notes by tag"),
            ("sort-by-tag",                         "Show all notes sorted by tag"),
        ],
        "OTHER": [
            ("hello",                               "Greeting"),
            ("help",                                "Show this help"),
            ("close / exit",                        "Save and exit"),
        ],
    }

    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=rich_box.SIMPLE_HEAD,
        pad_edge=True,
        show_lines=False,
        expand=False,
    )
    table.add_column("Command", style="bold white", min_width=42, no_wrap=True)
    table.add_column("Description", style="dim")

    first = True
    for section, commands in SECTIONS.items():
        if not first:
            table.add_row("", "")
        first = False
        table.add_row(f"[bold yellow]{section}[/bold yellow]", "")
        for cmd, desc in commands:
            table.add_row(f"  {escape(cmd)}", desc)

    console.print(
        Panel(table, title="[bold]Available Commands[/bold]", border_style="cyan")
    )


# ---------------------------------------------------------------------------
# Generic output
# ---------------------------------------------------------------------------

def ask() -> str:
    """Display the command prompt and return the raw user input."""
    return console.input("\n[bold cyan]>[/bold cyan] ")


def print_result(result: str) -> None:
    """Render a handler return value with colour-coding."""
    if not result or not result.strip():
        return
    if result.startswith("Error:"):
        console.print(f"[bold red]{result}[/bold red]")
    elif result.startswith("Usage:"):
        console.print(f"[yellow]{result}[/yellow]")
    elif result.startswith("No ") or "out of range" in result.lower():
        console.print(f"[dim]{result}[/dim]")
    elif "\n" not in result:
        # Short single-line affirmation → green
        console.print(f"[green]{result}[/green]")
    else:
        # Multi-line data (show-phones, show-birthday, etc.)
        console.print(result)


def print_info(msg: str) -> None:
    """Print a neutral informational message."""
    console.print(f"[dim]{msg}[/dim]")


def print_error(msg: str) -> None:
    """Print an error that originated outside a handler (UI layer)."""
    console.print(f"[bold red]Error: {msg}[/bold red]")


# ---------------------------------------------------------------------------
# Contact renderers
# ---------------------------------------------------------------------------

def show_contacts_table(records) -> None:
    """Render a list of Record objects as a rich Table."""
    if not records:
        print_info("No contacts found.")
        return
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=rich_box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Name",      style="bold white", min_width=14)
    table.add_column("Phones",    min_width=14)
    table.add_column("Emails",    min_width=22)
    table.add_column("Addresses", min_width=18)
    table.add_column("Birthday",  min_width=12)

    for record in records:
        table.add_row(
            record.name.value,
            "\n".join(p.value for p in record.phones)    or "—",
            "\n".join(e.value for e in record.emails)    or "—",
            "\n".join(a.value for a in record.addresses) or "—",
            str(record.birthday) if record.birthday else "—",
        )

    console.print(table)


def show_contact(record) -> None:
    """Render a single Record as a rich Panel."""
    lines = []
    for field in ("phones", "emails", "addresses"):
        items = getattr(record, field)
        if items:
            label = field.capitalize()
            numbered = "\n".join(
                f"  {i + 1}. {item.value}" for i, item in enumerate(items)
            )
            lines.append(f"[bold]{label}:[/bold]\n{numbered}")
    if record.birthday:
        lines.append(f"[bold]Birthday:[/bold] {record.birthday}")

    content = "\n".join(lines) if lines else "[dim]No details.[/dim]"
    console.print(
        Panel(
            content,
            title=f"[bold cyan]{record.name.value}[/bold cyan]",
            border_style="cyan",
        )
    )


# ---------------------------------------------------------------------------
# Note renderers
# ---------------------------------------------------------------------------

def show_note(note) -> None:
    """Render a single Note as a rich Panel."""
    tags_str = (
        "  ".join(f"[cyan]#{t.value}[/cyan]" for t in note.tags)
        if note.tags
        else "[dim]no tags[/dim]"
    )
    content = note.content or "[dim](empty)[/dim]"
    console.print(
        Panel(
            f"{content}\n\n[dim]Tags:[/dim] {tags_str}",
            title=f"[bold]{note.title}[/bold]",
            border_style="blue",
        )
    )


def show_notes(notes) -> None:
    """Render a list of Note objects as consecutive Panels."""
    notes = list(notes)
    if not notes:
        print_info("No notes available.")
        return
    for note in notes:
        show_note(note)
