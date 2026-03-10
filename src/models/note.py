from .fields import Tag


class Note:
    def __init__(self, title: str, content: str = ""):
        if not title or not title.strip():
            raise ValueError("Note title cannot be empty.")
        self.title = title.strip()
        self.content = content
        self._tags: list[Tag] = []

    @property
    def tags(self):
        return tuple(self._tags)

    def edit(self, new_content: str) -> None:
        pass  # TODO

    def add_tag(self, tag) -> None:
        pass  # TODO

    def remove_tag(self, tag_value: str) -> None:
        pass  # TODO

    def __str__(self):
        pass  # TODO
