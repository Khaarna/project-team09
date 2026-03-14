"""Tab-completion support for the Contact Book CLI."""

from prompt_toolkit.completion import Completer, Completion

_CONTACT_NAME_CMDS = frozenset({
    "delete", "info",
    "add-phone", "change-phone", "remove-phone", "show-phones",
    "add-email", "change-email", "remove-email", "show-emails",
    "add-address", "change-address", "remove-address", "show-addresses",
    "add-birthday", "change-birthday", "remove-birthday", "show-birthday",
})

_NOTE_TITLE_CMDS = frozenset({
    "note", "edit-note", "delete-note", "add-tag", "remove-tag",
})


class ContactBookCompleter(Completer):
    """Context-aware TAB completer.

    word_index 0 → registered command names
    word_index 1 → contact names or note titles, depending on the command
    """

    def __init__(self, ctx) -> None:
        self._ctx = ctx
        self._cmd_cache: list[str] | None = None

    def _commands(self) -> list[str]:
        # Built once: handler decorators run at import time, so by the first
        # TAB press both registries are fully populated.
        if self._cmd_cache is None:
            from .handlers.dispatcher import CONTACT_COMMANDS, NOTE_COMMANDS
            self._cmd_cache = sorted(
                set(CONTACT_COMMANDS) | set(NOTE_COMMANDS)
                | {"hello", "help", "close", "exit"}
            )
        return self._cmd_cache

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        trailing_space = text.endswith(" ")
        # 0 = typing the command, 1 = typing its first argument, 2+ = ignored
        word_index = max(0, len(words) - (0 if trailing_space else 1))
        prefix = "" if trailing_space else (words[-1] if words else "")

        if word_index == 0:
            for cmd in self._commands():
                if cmd.startswith(prefix.lower()):
                    yield Completion(cmd, start_position=-len(prefix))

        elif word_index == 1:
            cmd = words[0].lower()
            if cmd in _CONTACT_NAME_CMDS:
                candidates = (r.name.value for r in self._ctx.book)
            elif cmd in _NOTE_TITLE_CMDS:
                candidates = (n.title for n in self._ctx.notes)
            else:
                return
            for name in candidates:
                if name.lower().startswith(prefix.lower()):
                    yield Completion(name, start_position=-len(prefix))
