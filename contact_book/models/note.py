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
        self.content = new_content

    def add_tag(self, tag) -> None:
        tag_obj = tag if isinstance(tag, Tag) else Tag(tag)
        if tag_obj not in self._tags:
            self._tags.append(tag_obj)

    def remove_tag(self, tag_value: str) -> None:
        for index, tag in enumerate(self._tags):
            if tag.value == tag_value:
                del self._tags[index]
                return
        raise ValueError("Tag not found.")

    def __str__(self):
        tags = ", ".join(tag.value for tag in self._tags) if self._tags else "no tags"
        return f"Title: {self.title}\nContent: {self.content}\nTags: {tags}"
