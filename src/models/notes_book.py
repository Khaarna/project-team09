from .note import Note


class NotesBook:
    def __init__(self):
        self._notes: dict[str, Note] = {}

    def add(self, title: str, content: str = "") -> Note:
        pass  # TODO

    def find(self, title: str) -> Note:
        pass  # TODO

    def delete(self, title: str) -> None:
        pass  # TODO

    def edit(self, title: str, new_content: str) -> None:
        pass  # TODO

    def search(self, query: str) -> list[Note]:
        pass  # TODO

    def search_by_tag(self, tag: str) -> list[Note]:
        pass  # TODO

    def add_tag(self, title: str, tag: str) -> None:
        pass  # TODO

    def remove_tag(self, title: str, tag: str) -> None:
        pass  # TODO

    def all(self) -> str:
        pass  # TODO
