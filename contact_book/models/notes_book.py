from .note import Note


class NotesBook:
    def __init__(self):
        self._notes: dict[str, Note] = {}

    def add(self, title: str, content: str = "") -> Note:
        note = Note(title, content)
        key = note.title.lower()
        if key in self._notes:
            raise ValueError(f"Note '{title}' already exists.")
        self._notes[key] = note
        return note

    def find(self, title: str) -> Note:
        key = title.strip().lower()
        note = self._notes.get(key)
        if note is None:
            raise KeyError(f"Note '{title}' not found.")
        return note

    def delete(self, title: str) -> None:
        key = title.strip().lower()
        if key not in self._notes:
            raise KeyError(f"Note '{title}' not found.")
        del self._notes[key]

    def edit(self, title: str, new_content: str) -> None:
        self.find(title).edit(new_content)

    def search(self, query: str) -> list[Note]:
        needle = query.strip().lower()
        if not needle:
            return list(self._notes.values())
        return [
            note
            for note in self._notes.values()
            if needle in note.title.lower() or needle in note.content.lower()
        ]

    def search_by_tag(self, tag: str) -> list[Note]:
        needle = tag.strip().lower()
        if not needle:
            return []
        return [
            note
            for note in self._notes.values()
            if any(needle == note_tag.value.lower() for note_tag in note.tags)
        ]

    def sort_by_tag(self) -> list[Note]:
        def sort_key(note: Note):
            tags = sorted(t.value for t in note.tags)
            return (len(tags) == 0, tags)
        return sorted(self._notes.values(), key=sort_key)

    def add_tag(self, title: str, tag: str) -> None:
        self.find(title).add_tag(tag)

    def remove_tag(self, title: str, tag: str) -> None:
        self.find(title).remove_tag(tag)

    def all(self) -> str:
        if not self._notes:
            return "No notes available."
        return "\n\n".join(str(note) for note in self._notes.values())

    def __iter__(self):
        return iter(self._notes.values())
